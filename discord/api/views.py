import boto3
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,AllowAny
from .serializers import UserRegistrationSerializer
from rest_framework import generics,status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import ProfileModel,ProfileAvatar,ProfileAvatarIcon
from .serializers import ProfileSerializer,ProfileAvatarSerializer,ProfileAvatarIconSerializer
from datetime import timedelta
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenRefreshView   #come here again
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator


lambda_client=boto3.client('lambda',region_name=settings.AWS_S3_REGION_NAME)
sns_client=boto3.client('sns',region_name=settings.AWS_S3_REGION_NAME)
SNS_TOPIC_ARN=settings.AWS_SNS_ARN


def sns_publish(user):{
  sns_client.publish(
    TopicArn=SNS_TOPIC_ARN,
    Message=f'$Mr.{user.username} nice to see u here',
    Subject="New Profile"
  )
}

def trigger_lambda(event_data):
  response=lambda_client.invoke(
    FunctionName='Demo-studybud-drf',
    InvocationType='Event',
    Payload=json.dumps(event_data)
  )
  return response


class UserRegistrationView(generics.CreateAPIView):

  queryset= User.objects.all()
  serializer_class=UserRegistrationSerializer
  permission_classes=[AllowAny]

 # modifying the response so use create()
  def create(self, request, *args, **kwargs): 
  
    serializer=self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user=serializer.save()
    refresh=RefreshToken.for_user(user)
    sns_publish(user)

    response= Response({
      'user':{
        'id':user.id,
        'username':user.username,
        'email':user.email,
      },
  
    },
    status=status.HTTP_201_CREATED)


    cookie_max_age=7*24*60*60 #seconds 7 days in seconds
    response.set_cookie(
      key='refresh_token',
      value=str(refresh),
      httponly=True,
      secure=False,  #set to True only in prod
      samesite='Strict',
      max_age=cookie_max_age,
      expires=now()+timedelta(seconds=cookie_max_age)

  )
    response.set_cookie(
            'access',
            str(refresh.access_token),
            httponly=True,
            secure=False,  # Set to True in production
            samesite='Strict'
        )
    return response

class CookieTokenRefreshView(TokenRefreshView):
  serializer_class=TokenRefreshSerializer

  def post(self,request,*args,**kwargs):
    refresh_token=self.request.COOKIES.get('refresh')
    if refresh_token is None:
      return Response({'error':'Refresh token is missing'},status=400)
    
    serializer=self.get_serializer(data={'refersh':refresh_token})
    serializer.is_valid(raise_exception=True)
    return Response({'access':serializer.validated_data['access']})


@method_decorator(ensure_csrf_cookie,name='dispatch')
class CSRFTokenView(APIView):
  
  def get(self,request,format=None):
    return Response({'csrfToken':request.Meta.get('CSRF_COOKIE')})


class ProfileAvatarview(APIView):

  permission_classes=[IsAuthenticated]
  queryset =ProfileAvatar.objects.all()
  serializer_class=ProfileAvatarSerializer

  s3_client=boto3.client('s3',aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.AWS_S3_REGION_NAME
  )

  def get(self,request):
    user=self.request.user
    file_name=self.request.GET.get('file_name')
  
    presigned_urls=self.s3_client.generate_presigned_url(
      'put_object',
      Params={'Bucket':settings.AWS_STORAGE_BUCKET_NAME,'Key':f'{user}/{file_name}'},
      ExpiresIn=3600
    )
    url=f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{user}/{file_name}'
    
    return Response({'upload_url':presigned_urls ,'file_url':url,'bucket':settings.AWS_STORAGE_BUCKET_NAME,'key':f'{user}/{file_name}'})
  
  def put(self,request):
    
    user=request.user
    data=request.data
    bucket=data.pop('bucket')
    key=data.pop('key')
    data2={'url':data.get('profile_avatar'),'bucket':bucket,'key':key,'user':user.id}
    avatar,created=ProfileAvatar.objects.get_or_create(user=user)
    serializer=ProfileAvatarSerializer(avatar,data=request.data)

    if serializer.is_valid():
      serializer.save()
      trigger_lambda(data2)
      return Response(serializer.data,status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

                                                        
class PublicProfile(APIView):

  permission_classes=[AllowAny]
  queryset =ProfileModel.objects.all()

  def get(self,request,user_id):
    
    try:
      user=User.objects.get(id=user_id)
    except User.DoesNotExist:
     
     return Response(
       {'error':'user not found'},
       status=status.HTTP_404_NOT_FOUND
     )

    profile,create=ProfileModel.objects.get_or_create(user=user)
    serializer=ProfileSerializer(profile,context={'request': request})
    return Response(serializer.data)


class Profile(APIView):

  permission_classes=[IsAuthenticated]
  queryset =ProfileModel.objects.all()
  serializer_class=ProfileSerializer
  
  def get(self,request):
    user=self.request.user
    profile,create=ProfileModel.objects.get_or_create(user=user)
    serializer=ProfileSerializer(profile,context={'request': request})
    
    return Response(serializer.data)
  
  def put(self,request):
    user=self.request.user
    profile,created=ProfileModel.objects.get_or_create(user=user)
    serialilzer=ProfileSerializer(profile,data=request.data,context={'request': request})
    if serialilzer.is_valid():
      serialilzer.save()
      
      return Response(serialilzer.data,status=status.HTTP_200_OK)
    return Response(serialilzer.errors,status=status.HTTP_400_BAD_REQUEST)
  

class ProfileAvatarIconview(APIView):
  permission_classes=[AllowAny]

  def put(self,request):
    user=self.request.data.get('user')
    avatar,created=ProfileAvatarIcon.objects.get_or_create(user=user)
 
    serializer=ProfileAvatarIconSerializer(avatar,data=request.data,context={'request':request})
    if serializer.is_valid():
      serializer.save()

      return Response(serializer.data,status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    
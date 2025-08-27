import boto3
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,AllowAny
from .serializers import UserRegistrationSerializer
from rest_framework import generics,status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import ProfileModel,ProfileAvatar
from .serializers import ProfileSerializer,ProfileAvatarSerializer


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

    return Response({
      'user':{
        'id':user.id,
        'username':user.username,
        'email':user.email,
      },
      'refresh':str(refresh),
      'access':str(refresh.access_token)
    },
    status=status.HTTP_201_CREATED)


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
    
    return Response({'upload_url':presigned_urls ,'file_url':url})
  
  def put(self,request):
    
    user=request.user
    avatar,created=ProfileAvatar.objects.get_or_create(user=user)
    serializer=ProfileAvatarSerializer(avatar,data=request.data)

    if serializer.is_valid():
      serializer.save()
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
  

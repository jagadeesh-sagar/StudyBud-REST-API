from .serializers import UserRegistrationSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


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

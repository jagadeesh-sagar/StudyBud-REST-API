from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import ProfileModel,ProfileAvatar,ProfileAvatarIcon


class Userserializer(serializers.ModelSerializer):

  class Meta:
    model=User
    fields=['id','username']

class UserRegistrationSerializer(serializers.ModelSerializer):

  password=serializers.CharField(write_only=True,validators=[validate_password])
  confirm_password=serializers.CharField(write_only=True)
  
  class Meta:
    model=User  
    fields=['username','first_name','last_name','email','password','confirm_password']

  def validate(self, attrs):
    if attrs['password']!=attrs['confirm_password']:
      raise serializers.ValidationError('Passwords does not match')
    
      # Check if username already exists
    if User.objects.filter(username=attrs['username']).exists():
      raise serializers.ValidationError('Username already exists.')
    
    return attrs

  def create(self, validated_data):

    user = User.objects.create_user(
    username=validated_data['username'],
    first_name=validated_data.get('first_name', ''),
    last_name=validated_data.get('last_name', ''),
    email=validated_data['email'],
    password=validated_data['password'],
)
    return user


class ProfileAvatarSerializer(serializers.ModelSerializer):

  user=Userserializer(read_only=True)
  class Meta:
    model=ProfileAvatar
    fields=['user','profile_avatar']
  
  def update(self, instance, validated_data):
    instance.profile_avatar=validated_data.get('profile_avatar',instance.profile_avatar)
    instance.save()
    return instance


class ProfileAvatarIconSerializer(serializers.ModelSerializer):

  user=Userserializer(read_only=True)

  class Meta:
    model=ProfileAvatarIcon
    fields=['user','profile_avatar_icon']

  def update(self, instance, validated_data):
    instance.profile_avatar_icon=validated_data.get('profile_avatar_icon',instance.profile_avatar_icon)
    instance.save()
    return instance
  

class ProfileSerializer(serializers.ModelSerializer):

  user=Userserializer(read_only=True)
  avatar_url=serializers.SerializerMethodField(read_only=True)
  avatar_icon_url=serializers.SerializerMethodField(read_only=True)
  
  class Meta:
    model=ProfileModel
    fields=['user','bio','avatar_url','avatar_icon_url']

  def get_avatar_url(self,obj):
    request=self.context.get('request')

    if request is None:
      return None
    avatar,create=ProfileAvatar.objects.get_or_create(user=obj.user)

    if avatar.profile_avatar:
      return avatar.profile_avatar
    else:
      return None
   
  def get_avatar_icon_url(self,obj):
    request=self.context.get('request')

    if request is None:
      return None
    avatar,create=ProfileAvatarIcon.objects.get_or_create(user=obj.user)

    if avatar.profile_avatar_icon:
      return avatar.profile_avatar_icon
    else:
      return None
   
  def update(self, instance, validated_data):
    instance.bio = validated_data.get('bio', instance.bio)
    instance.save()
    return instance
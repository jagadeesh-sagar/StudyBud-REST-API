from django.db import models
from django.contrib.auth.models import User


class ProfileModel(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE,null=False)
  bio=models.TextField(max_length=400,null=True,blank=True)


class ProfileAvatar(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE,null=False)
  profile_avatar=models.URLField(max_length=200,blank=True,null=True)


class ProfileAvatarIcon(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE,null=False)
  profile_avatar_icon=models.URLField(max_length=200,blank=True,null=True)

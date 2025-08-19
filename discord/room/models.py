from django.db import models
from django.contrib.auth.models import User


class Topics(models.Model):
  name=models.CharField(max_length=200)

class Room(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE,null=False)
  topic=models.ForeignKey(Topics,on_delete=models.CASCADE,null=False)
  name=models.CharField(max_length=200)
  body=models.TextField(max_length=200,blank=True)
  participants=models.ManyToManyField(User,related_name='participants',blank=True)
  updated=models.DateTimeField(auto_now=True) #can be modifed
  created=models.DateTimeField(auto_now_add=True) #fixed


class Message(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE,null=False)
  room=models.ForeignKey(Room,on_delete=models.CASCADE,null=False)
  body=models.CharField(max_length=200,null=False)
  updated=models.DateTimeField(auto_now=True)
  created=models.DateTimeField(auto_now_add=True) 

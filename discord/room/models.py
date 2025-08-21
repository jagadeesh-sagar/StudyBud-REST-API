from django.db import models
from django.contrib.auth.models import User
# User=settings.AUTH_USER_MODEL


class Topics(models.Model):
  name=models.CharField(max_length=200)

  @property
  def topic(self):
    return self.name

  def __str__(self):
    return self.name


class Room(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE,null=False)
  topic=models.ForeignKey(Topics,on_delete=models.CASCADE,null=False)
  name=models.CharField(max_length=200)
  body=models.TextField(max_length=200,blank=True)
  participants=models.ManyToManyField(User,related_name='participants',blank=True)
  updated=models.DateTimeField(auto_now=True) #can be modifed
  created=models.DateTimeField(auto_now_add=True) #fixed
  
  # @property
  # def username(self):
  #   return self.user.username

  @property
  def get_topic_name(self):
    return self.topic.name
  
  def __str__(self):
    return self.name


class Message(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE,null=False)
  room=models.ForeignKey(Room,on_delete=models.CASCADE,null=False)
  body=models.CharField(max_length=200,null=False)
  updated=models.DateTimeField(auto_now=True)
  created=models.DateTimeField(auto_now_add=True) 

  @property
  def get_room_name(self):
    return self.room.name
  
  @property
  def get_room_id(self):
    return self.room

  def __str__(self):
    return self.body



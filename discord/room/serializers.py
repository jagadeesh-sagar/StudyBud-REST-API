from  rest_framework import serializers
from rest_framework.reverse import reverse
from . import models
from django.contrib.auth.models import User


class UserSerializers(serializers.ModelSerializer):

   class Meta:
      model=User
      fields=['id','username']


class TopicsSerializers(serializers.ModelSerializer):
   topic=serializers.CharField(source="name")
   endpoint=serializers.SerializerMethodField()

   class Meta:
      model=models.Topics
      fields=['id','topic','endpoint']

   def get_endpoint(self,obj):
      request=self.context.get('request')
      if request is None:
         return None
      url=reverse('room-list',request=request)
      return f'{url}?q={obj.id}'


class MessageSerializers(serializers.ModelSerializer):
   user=UserSerializers(read_only=True)
   room_name=serializers.CharField(source='room',read_only=True)
   endpoint=serializers.SerializerMethodField()

   class Meta:
      model=models.Message
      fields=['id','user','room','room_name','body','updated','created','endpoint',]
      read_only_fields=['id','updated','created']

   def get_endpoint(self,obj):
      request=self.context.get('request')
      if request is None:
         return None
      return reverse('room-detail',kwargs={"pk":obj.room.pk},request=request)
   
   def create(self, validated_data):
 
         message=super().create(validated_data)
         room =message.room
         user=message.user
         if user not in room.participants.all():
             
           room.participants.add(user)
   
         return message


class RoomSerializers(serializers.ModelSerializer):

   user=UserSerializers(read_only=True)
   topic=TopicsSerializers(read_only=False)
   participants = UserSerializers(many=True, read_only=True)
   message=MessageSerializers(read_only=True)
   endpoint=serializers.HyperlinkedIdentityField(view_name="room-detail",lookup_field='pk')
   # topic_name=serializers.CharField(source='name',read_only=True) 

  
   class Meta:
      model=models.Room
      fields=['id','user',"topic","name","body","participants","updated","created",'message','endpoint']#,'topic_name']#'user_name',]
      read_only_fields=['id','updated','created']
    
   def create(self, validated_data):
        topic_data = validated_data.pop('topic')
        topic_name = topic_data['name']   # it is in the form of {'name': 'biology'} so we used this (nested json)
        topic, created = models.Topics.objects.get_or_create(name=topic_name)
        validated_data['topic'] = topic
        return models.Room.objects.create(**validated_data)
   
   def update(self,instance, validated_data): # instance is neccessary so that it retriews old one and update that
        topic_data = validated_data.pop('topic')
        topic_name = topic_data['name']   # it is in the form of {'name': 'biology'} so we used this (nested json)
        topic, created = models.Topics.objects.get_or_create(name=topic_name)
  
        instance.topic=topic
        instance.name=validated_data.get('name',  instance.name)
      #   instance.name=instance.name.upper()
        instance.body=validated_data.get('body',  instance.body)
        instance.save()
        return instance
      #   return super().update(instance,validated_data) if i use this then name , body will automatically hanlde by drf
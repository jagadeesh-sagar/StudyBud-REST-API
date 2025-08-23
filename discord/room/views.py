from rest_framework import generics
from . import serializers
from . import models
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .permissions import IsOwnerOrReadOnly


class RoomListAPIView(generics.ListCreateAPIView):
  queryset = models.Room.objects.all()
  serializer_class=serializers.RoomSerializers

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

  def get_queryset(self,*args,**kwargs):
    query=self.request.GET.get('q')
   
    if not query:
         return super().get_queryset()

    qs= super().get_queryset()
    qs_name=qs.filter( Q(name__contains=query))

    if query.isdigit():
      qs_topic=qs.filter( Q(topic_id=int(query)))
      return (qs_name | qs_topic).distinct()
      
    return qs_name
  
room_list_create_view=RoomListAPIView.as_view()


class RoomDetailAPIVIew(generics.RetrieveAPIView):
  queryset=models.Room.objects.all()
  serializer_class=serializers.RoomSerializers

room_detail_view=RoomDetailAPIVIew.as_view()


class RoomUpdateAPIView(generics.UpdateAPIView,viewsets.ModelViewSet):
  queryset=models.Room.objects.all()
  serializer_class=serializers.RoomSerializers
  permission_classes=[IsOwnerOrReadOnly]


  def perform_update(self, serializer):
    serializer.save(user=self.request.user)

room_update_view=RoomUpdateAPIView.as_view()


class RoomDeleteAPIView(generics.DestroyAPIView,viewsets.ModelViewSet):
  queryset=models.Room.objects.all()
  serializer_class=serializers.RoomSerializers
  permission_classes=[IsOwnerOrReadOnly]

room_delete_view=RoomDeleteAPIView.as_view()


class MessageAPIView(generics.ListCreateAPIView):
  queryset=models.Message.objects.all()
  serializer_class=serializers.MessageSerializers


  def perform_create(self,serializer):
    print(self.request)
    serializer.save(user=self.request.user)

message_list_view=MessageAPIView.as_view()


class TopicsAPIView(generics.ListAPIView):
  queryset=models.Topics.objects.all()
  serializer_class=serializers.TopicsSerializers

topics_list_view=TopicsAPIView.as_view()

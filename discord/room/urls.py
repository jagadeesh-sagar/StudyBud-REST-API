from . import views
from django.urls import path ,include

urlpatterns=[
  path('',views.room_list_create_view,name='room-list'),
  path('<int:pk>/',views.room_detail_view,name='room-detail'),
  path('update/<int:pk>/',views.room_update_view,name='room-update'),
  path('delete/<int:pk>/',views.room_delete_view,name='room-delete'),
  path('message/',views.message_list_view,name='message-list'),
  path('topics/',views.topics_list_view,name='topics-list'),
]
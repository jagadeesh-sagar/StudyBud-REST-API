from django.urls import path
from . import views

urlpatterns=[
  path('register/', views.UserRegistrationView.as_view(),name='register' ),
  path('profile/', views.Profile.as_view(),name='Profile' ),
  path('profile/<int:user_id>/', views.PublicProfile.as_view(),name='Profile' ),
  path('profile/avatar/', views.ProfileAvatarview.as_view(),name='Avatar' ),
]
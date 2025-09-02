from django.urls import path
from . import views

urlpatterns=[
  path('register/', views.UserRegistrationView.as_view(),name='register' ),
  path('refresh/', views.CookieTokenRefreshView.as_view(),name='refresh' ),
  path('csrf-token/', views.CSRFTokenView.as_view(), name='csrf-token'),
  path('profile/', views.Profile.as_view(),name='Profile' ),
  path('profile/<int:user_id>/', views.PublicProfile.as_view(),name='Profile' ),
  path('profile/avatar/', views.ProfileAvatarview.as_view(),name='Avatar' ),
  path('profile/avatar/icon/', views.ProfileAvatarIconview.as_view(),name='Avatar_ico' ),
]
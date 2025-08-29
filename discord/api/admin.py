from django.contrib import admin

# Register your models here.
from .models import ProfileAvatar,ProfileModel,ProfileAvatarIcon

admin.site.register(ProfileAvatar)
admin.site.register(ProfileModel)
admin.site.register(ProfileAvatarIcon)
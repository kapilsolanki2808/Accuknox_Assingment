from django.contrib import admin
from . models import UserModel,FriendRequestModel
# Register your models here.
admin.site.register(UserModel)
admin.site.register(FriendRequestModel)
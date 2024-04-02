from rest_framework import serializers
from .models import UserModel,FriendRequestModel


class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)
  class Meta:
    model = UserModel
    fields = ['id','name','email','password']



class FriendRequestSerializer(serializers.ModelSerializer):
  class Meta:
    model = FriendRequestModel
    fields = ['id','request_to','request_from','status']

  def to_representation(self, instance):
        data = super(FriendRequestSerializer, self).to_representation(instance)
        data['request_to'] = instance.request_to.name       
        return data  
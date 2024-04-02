from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# Create your models here.


class UserModel(AbstractUser):
  username = models.CharField(max_length=250, null=True, blank=True, unique=True)
  email = models.EmailField(max_length=255, unique=True)
  name = models.CharField(max_length=255, null=True, blank=True)

  def save(self, *args, **kwargs):
    self.username = self.email
    super(UserModel, self).save(*args, **kwargs)
  
  def __str__(self):
    return str(self.name)

choice = (('PENDING', 'PENDING'),('REJECT', 'REJECT'),('ACCEPTED', 'ACCEPTED'))


class FriendRequestModel(models.Model):
  request_from = models.ForeignKey(UserModel, on_delete=models.CASCADE,related_name='friend_request_from',null=True,blank=True)
  request_to = models.ForeignKey(UserModel, on_delete=models.CASCADE,related_name='friend_request_to',null=True,blank=True)
  status = models.CharField(max_length = 250, default='PENDING',choices=choice)

  def __str__(self):
    return str(self.request_to.username)
  
  def clean(self):
        if self.request_from == self.request_to:
            raise ValidationError("A user cannot send a friend request to themselves.")
        super().clean()

   
     
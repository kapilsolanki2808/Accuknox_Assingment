from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

from django.db import models
from django.conf import settings

class Profile(AbstractUser):
    choice = (("MALE", "MALE"), ("FEMALE", "FEMALE"), ("OTHER", "OTHER"))
    username = models.CharField(max_length=250, null=True, blank=True, unique=True)
    name = models.CharField(max_length=100,null=True, blank=True)
    email = models.EmailField(max_length=250, unique=True)
    gender = models.CharField(max_length=250, default="", choices=choice)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class FriendRequestModel(models.Model):
    choice = (("PENDING", "PENDING"), ("REJECT", "REJECT"), ("ACCEPTED", "ACCEPTED"))
    request_from = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="friend_request_from",
        null=True,
        blank=True,
    )
    request_to = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="friend_request_to",
        null=True,
        blank=True,
    )
    status = models.CharField(max_length=250, default="PENDING", choices=choice)

    def __str__(self):
        return str(self.request_to.username)

    def clean(self):
        if self.request_from == self.request_to:
            raise ValidationError("A user cannot send a friend request to themselves.")
        super().clean()


class FriendList(models.Model):
    you = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="friends",
        null=True,
        blank=True,
    )
    friend = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="friend_of",
        null=True,
        blank=True,
    )

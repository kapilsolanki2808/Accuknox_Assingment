from django.urls import path
from . views import *


urlpatterns = [
              path('register/',RegisterUserView.as_view()),
              path('login/',Login.as_view()),
              path('search/',UserSearchAPIView.as_view()),
              path('my/friends/',MyFriendListView.as_view()),
              path('send/request/',SendFriendRequestAPIView.as_view()),
              path('reject_or_accept/',AcceptOrRejectFriendRequestAPIView.as_view()),
              path('accepted/request/',AcceptedFriendRequest.as_view()),
              path('reject_or_accept/<int:id>/',AcceptOrRejectFriendRequestAPIView.as_view()),
]



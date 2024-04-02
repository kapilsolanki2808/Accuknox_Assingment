from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from .serializer import *
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth import login, authenticate
from rest_framework import status
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework import generics
from .models import FriendRequestModel
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.throttling import UserRateThrottle


# Create your views here.

class RegisterUserView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        queryset = UserModel.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):   
        data = request.data
        data['is_staff'] = True  
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            new_user.set_password(data['password'])
            new_user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class Login(APIView):
    def post(self, request):
      email = request.data.get('email')
      password = request.data.get('password')
      user = authenticate(request, username=email, password=password)
      if user is not None:
          login(request, user)
          return Response({'success': "Login successful"},status=status.HTTP_200_OK)
      return Response({"failed" : "Login failed"}, status=status.HTTP_401_UNAUTHORIZED)


class UserSearchAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    pagination_class = [PageNumberPagination]

    def get(self,request,pk=None):
        email = self.request.data.get('email')
        name = self.request.data.get('name')
        if email is not None or name is not None:
            queryset = UserModel.objects.all()
            if email:
                queryset = queryset.filter(username=email)
            if name:
                queryset = queryset.filter(name__icontains=name.strip())
            serilaizer = UserSerializer(queryset,many=True)
            return Response(serilaizer.data,status=status.HTTP_200_OK )
        return Response("data does not exist")


class FriendRequestThrottle(UserRateThrottle):
    scope = 'friend_request'

class SendFriendRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [FriendRequestThrottle]
    def post(self, request):
      request_to = request.data.get('request_to')
      serializer = FriendRequestSerializer(data=request.data)
      if serializer.is_valid():
          req = serializer.save()
          req.request_from = request.user
          queryset = FriendRequestModel.objects.filter(Q(request_from=request.user) & Q(request_to=request_to)).first()
          if not queryset:
            req.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
          return Response("all ready exist")
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RejectFriendRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id=None):
        if id is not None:
            obj = get_object_or_404(FriendRequestModel, id=id)
            serializer = FriendRequestSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            friend_request = FriendRequestModel.objects.filter(Q(request_to=request.user) & Q(status='PENDING'))
            serializer = FriendRequestSerializer(friend_request, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK) 

    def patch(self, request,id):
        friend_request = get_object_or_404(FriendRequestModel,id=id)
        serializer = FriendRequestSerializer(instance=friend_request,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            del_reject_request = FriendRequestModel.objects.filter(status = "REJECT")
            del_reject_request.delete()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)          

class AcceptedFriendRequest(APIView):
    permission_classes = [IsAuthenticated]         
    def get(self, request, id=None):
        friend_request = FriendRequestModel.objects.filter(Q(request_from=request.user) & Q(status='ACCEPTED'))
        serializer = FriendRequestSerializer(friend_request, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .serializer import *
from rest_framework.views import APIView
from django.contrib.auth import login, authenticate
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import UserRateThrottle
import django_filters
from rest_framework import filters
from rest_framework import status, generics

# Create your views here.


class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = UserModel.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        data["is_staff"] = True
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            new_user.set_password(data["password"])
            new_user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return Response({"success": "Login successful"}, status=status.HTTP_200_OK)
        return Response({"failed": "Login failed"}, status=status.HTTP_401_UNAUTHORIZED)




class UserSearchAPIView(generics.ListAPIView):
    pagination_class = PageNumberPagination
    page_size = 10
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name__icontains", "=email"]


class FriendRequestThrottle(UserRateThrottle):
    scope = "friend_request"


class SendFriendRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [FriendRequestThrottle]

    def post(self, request):
        request_to = request.data.get("request_to")
        serializer = FriendRequestSerializer(data=request.data)
        if serializer.is_valid():
            req = serializer.save()
            req.request_from = request.user
            if request_to == request.user.id:
                return Response("can not send friend request to yourself")
            if (
                not FriendRequestModel.objects.filter(
                    request_to=request.user, request_from=request_to
                ).exists()):
                queryset = FriendRequestModel.objects.filter(
                    request_from=request.user, request_to=request_to
                ).first()
                if not queryset:
                    req.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response("all ready exist")
            return Response(f"you have friend request from {request_to} ")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AcceptOrRejectFriendRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id is not None:
            obj = get_object_or_404(FriendRequestModel, id=id)
            serializer = FriendRequestSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            friend_request = FriendRequestModel.objects.filter(
                Q(request_to=request.user) & Q(status="PENDING")
            )
            serializer = FriendRequestSerializer(friend_request, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        friend_request = get_object_or_404(FriendRequestModel, id=id)
        serializer = FriendRequestSerializer(
            instance=friend_request, data=request.data, partial=True
        )
        if serializer.is_valid():
            status_value = serializer.validated_data.get("status")
            if status_value == "ACCEPTED":
                # Create FriendList object
                FriendList.objects.create(you=friend_request.request_from, friend=friend_request.request_to)
            serializer.save()
            del_reject_request = FriendRequestModel.objects.filter(status="REJECT")

            del_reject_request.delete()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)
    # def patch(self, request, id):
    #     friend_request = get_object_or_404(FriendRequestModel, id=id)
    #     serializer = FriendRequestSerializer(
    #         instance=friend_request, data=request.data, partial=True
    #     )
    #     if serializer.is_valid():
    #         status_value = serializer.validated_data.get("status")
    #         if status_value == "Accepted":
    #             # Create FriendList object
    #             FriendList.objects.create(you=friend_request.from_user, friend=friend_request.to_user)
            
    #         serializer.save()
    #         # Delete rejected friend requests
    #         del_reject_request = FriendRequestModel.objects.filter(status="REJECT")
    #         del_reject_request.delete()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(status=status.HTTP_204_NO_CONTENT)

class AcceptedFriendRequest(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        friend_request = FriendRequestModel.objects.filter(
            Q(request_from=request.user) & Q(status="ACCEPTED")
        )
        serializer = FriendRequestSerializer(friend_request, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyFriendListView(APIView):
    def get(self, request):
        queryset = FriendList.objects.filter(Q(you=request.user)| Q(friend = request.user))
        serializers = MyFriendListSerializer(queryset, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
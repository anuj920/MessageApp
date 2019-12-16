from django.shortcuts import render

from rest_framework.views import APIView
from .serializers import MessageSerializer
from normal.models import Message
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.generics import DestroyAPIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token



class AddMessage(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(user = self.request.user)


class MessageOperation(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super(MessageOperation, self).get_serializer(*args, **kwargs)

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user, pk=int(self.kwargs.get("pk")))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        all_data = dict(request.data)
        serializer = self.get_serializer(instance, data=all_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class Register(APIView):

    def post(self, request):
        password1 = request.data.get("password")
        password2 = request.data.get("confirm_password")
        email = request.data.get("email")
        user = request.data.get("user")
        if password1 and password2 and password2 == password1:
            if user:
                user_exists = User.objects.filter(username=user).exists()
                if user_exists:
                    return Response({"message": "User with this User Name already exists.", "flag": False},status=status.HTTP_400_BAD_REQUEST)
                else:
                    user = User.objects.create_user(username=user, password=password1, email=email)
                    user.is_active = False
                    user.save()
                    return Response({"message": "User Register Successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Please check the form filled."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Please fill Details"}, status=status.HTTP_201_CREATED)


class Logout(DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.auth


class Login(APIView):
    
    def post(self, request):
        name = request.data.get("username")
        password = request.data.get("password")
        # print(name,password)
        try:
            user_exists = User.objects.filter(username=name)
            if not user_exists.exists():
                return Response({"message": "User with this details not exists.", "flag": False},status=status.HTTP_400_BAD_REQUEST)
            user_obj = authenticate(username=user_exists[0].username, password=password)
            if user_obj:
                if user_obj.is_active:
                    user_token, created=Token.objects.get_or_create(user=user_obj)
                    return Response({"message":"Logged in","username":user_obj.username,"token":user_token.key},status=status.HTTP_200_OK)
            else:
                return Response({"message": 'Password Incorrect', "flag": False}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response(
                {'message': 'Please enter a valid username and password.', "details": str(e), "flag": False},status=status.HTTP_401_UNAUTHORIZED)


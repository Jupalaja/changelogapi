from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.generics import GenericAPIView
from rest_framework import status, response, permissions

import authentication.jwt
from authentication.serializers import RegisterSerializer, LoginSerializer


class AuthUserAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user)
        return response.Response({'user': serializer.data})


class RegisterApiView(GenericAPIView):
    serializer_class = RegisterSerializer
    authentication_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(GenericAPIView):
    serializer_class = LoginSerializer
    authentication_classes = []

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = authenticate(email=email, password=password)

        if user:
            serializer = self.serializer_class(user)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response({"message": "Invalid credentials, try again"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutApiView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        request.user.token.delete()
        return response.Response({"success": "Successfully logged out"},
                                 status=status.HTTP_200_OK)

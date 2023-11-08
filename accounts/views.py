from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.serializers import UserSerializer, UserLoginSerializer, UserProfileSerializer, UserChangePasswordSerializer, ForgotPasswordSerializer, ResetPasswordSerializer 

# Create your models here.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class CreateAccount(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({"token":token,"msg":"User created Successfully!"},  status=status.HTTP_201_CREATED)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)

                return Response({"token":token ,"msg":"Login SuccessFull"}, status=status.HTTP_202_ACCEPTED)    
            else:
                return Response({"error":"Email/Password is not correct"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class UserProfileView(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)

        return Response(serializer.data)
    
class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"msg":"password changed Successfully."})
        return Response(serializer.errors)


class ForgotPassword(APIView):
    def post(self, request, format=None):        
        serializer = ForgotPasswordSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"msg":"An email is sent to your email address."})
        return Response(serializer.errors)
    


class ResetPassword(APIView):
    
    def post(self, request, uid, token,  format=None):        
        serializer = ResetPasswordSerializer(data=request.data, context = {"uid":uid, "token":token})
        
        if serializer.is_valid(raise_exception=True):
            return Response({"msg":"Password Changed Successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
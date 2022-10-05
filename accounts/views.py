import re
from .serializers import *
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
#import schema view from drf_yasg
from drf_yasg.utils import swagger_auto_schema
#import send mail
from django.core.mail import send_mail
import random
import hashlib
from datetime import datetime as dt, timedelta as td
import string
from django.utils import timezone
from django.conf import settings
from drf_yasg import openapi


User = get_user_model()

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny,]
    @swagger_auto_schema(
        responses = {
            200: 'User Created', 
            400: 'Bad Request'
        },
        operation_summary = 'Register (No Auth Required)',
        operation_description = 'Register a new user with email, first_name, last_name, password, password2, phone fields. (Need To Login to get the access and refresh token)',
        operation_id = 'register',
        tags=['Accounts'],
        request_body = RegisterSerializer
        )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })
    
class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    permission_classes = [AllowAny,]

    @swagger_auto_schema(
        operation_summary = 'Login (No Auth Required)',
        operation_description = 'Login a user with email and password fields. (returns 2 tokens access "valid for 5 days" and refresh "valid for 10 days" the user can choose if he wants to use refresh token or not)',
        operation_id = 'Login',
        tags=['Accounts'],
        responses={
            200: LoginResponseSerializer,
            400: 'Bad Request',
            401: 'Unauthorized',
            403: 'Forbidden',
            404: 'Not Found',
            500: 'Internal Server Error',
        },
        request_body = TokenObtainPairSerializer
    )
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=request.data['email'])
        refresh = RefreshToken.for_user(user)
        access = AccessToken.for_user(user)
        return Response({
            "access": str(access),
            "refresh": str(refresh),
            "user": UserSerializer(user, context=self.get_serializer_context()).data
        })

class ConfirmEmailView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ConfirmEmailSerializer
    
    @swagger_auto_schema(
        responses = {
            200: 'Token sent to email', 
            400: 'Invalid email',
            302: 'Email already confirmed'
        }, 
        operation_summary = 'Send Token to Email (Auth Required)',
        operation_description = 'Send confirmation token to user email to confirm email using post request the token is valid for 10 minutes',
        operation_id = 'send_token_to_email',
        tags=['Accounts Utils'],
    )
    def get(self, request, *args, **kwargs):
        if request.user.email_confirmed:
            return Response({
                'message': 'Email already confirmed'
            },status=status.HTTP_302_FOUND)

        try:
            token = random.Random().randint(111111, 999999)
            user = request.user
            send_mail(
                'Confirm your email',
                f'Your confirmation code is {token}',
                'mateus@horizon-development.com',
                [user.email],
                fail_silently=False,
            )
            token = hashlib.sha256(str(self.token).encode('utf-8')).hexdigest()
            user.email_token = token
            user.email_datetime_validator = dt.now() + td(minutes=10)
            user.save()
            return Response({
                'message': 'Email sent successfully',   
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message': 'Error sending email',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        responses = {
            200: 'Email confirmed', 
            400: 'Invalid token', 
            301: 'Token expired',
            302: 'Email already confirmed'
        },
        operation_summary = 'Confirm email (Auth Required)',
        operation_description =  'Confirm email using token sent to user email using post request. The token is valid for 10 minutes',
        operation_id = 'confirm_email',
        tags=['Accounts Utils'],
    )
    def post(self, request, *args, **kwargs):
        if request.user.email_confirmed:
            return Response({
                'message': 'Email already confirmed'
            },status=status.HTTP_302_FOUND)

        try:
            user = request.user
            token = hashlib.sha256(str(request.data.get('token')).encode('utf-8')).hexdigest()
            if user.email_token == token:
                if user.email_datetime_validator > dt.now():
                    user.email_confirmed = True
                    user.save()
                    return Response({
                        'message': 'Email confirmed successfully',
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'message': 'Token expired',
                    }, status=status.HTTP_301_MOVED_PERMANENTLY)
            else:
                return Response({
                    'message': 'Token invalid',
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'message': str(e),
                'pow': False
            })

class ConfirmPhoneView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ConfirmPhoneSerializer

    @swagger_auto_schema(
        responses = {
            200: 'Token sent to phone', 
            400: 'Invalid phone', 
            302: 'Phone already confirmed'
        },
        operation_summary = 'Send token to phone (Auth Required)',
        operation_description = 'Send token to user phone to confirm phone using post request. The token is valid for 10 minutes',
        operation_id = 'send_token_to_phone',
        tags=['Accounts Utils'],

    )
    def get(self, request, *args, **kwargs):
        if request.user.phone_confirmed:
            return Response({
                'message': 'Phone already confirmed',
            }, status=status.HTTP_302_FOUND)
        try:
            token = random.Random().randint(111111, 999999)
            user = request.user
            
            def send_sms(phone, message): #send sms hook
                pass

            send_sms(user.phone, f'Your confirmation code is {token}')
            token = hashlib.sha256(str(token).encode('utf-8')).hexdigest()
            user.phone_token = token
            user.phone_datetime_validator = dt.now() + td(minutes=10)
            user.save()
            return Response({
                'message': 'SMS sent successfully',
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                'message': 'SMS not sent',
            }, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses = {
            200: 'Phone confirmed', 
            400: 'Invalid token', 
            301: 'Token expired', 
            302: 'Phone already confirmed'
        },
        operation_summary = 'Confirm Phone (Auth Required)',
        operation_description = 'Confirm phone token sent to user phone using post request. The token is valid for 10 minutes',
        operation_id = 'confirm_phone',
        tags=['Accounts Utils'],
    )
    def post(self, request, *args, **kwargs):
        if request.user.phone_confirmed:
            return Response({
                'message': 'Phone already confirmed',
            }, status=status.HTTP_302_FOUND)
        try:
            user = request.user
            token = hashlib.sha256(str(request.data.get('token')).encode('utf-8')).hexdigest()
            if user.phone_token == token:
                if user.phone_datetime_validator > dt.now():
                    user.phone_confirmed = True
                    user.save()
                    return Response({
                        'message': 'Phone confirmed successfully',
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'message': 'Token expired',
                }, status=status.HTTP_301_MOVED_PERMANENTLY)
        except Exception as e:
            return Response({
                'message': str(e),
            }, status=status.HTTP_400_BAD_REQUEST)

 
class ResetPasswordView(generics.GenericAPIView):
    permission_classes = [AllowAny,]
    serializer_class = ResetPasswordSerializer,

    @swagger_auto_schema(
        responses = {
            200: 'Token sent to email', 
            400: 'Invalid email',
            404: 'User not found',
        }, 
        operation_summary = 'Send Reset Password Token (Auth Not Required)',
        operation_description = 'Send confirmation token to user email to allow edit password using post request. The token is valid for 10 minutes',
        operation_id = 'send_reset_password_token',
        tags=['Accounts Utils'],
        manual_parameters = [openapi.Parameter('email', openapi.IN_QUERY, description='User email', type=openapi.TYPE_STRING)]
    )
    def get(self, request, *args, **kwargs):
        if not request.GET.get('email'):
            return Response({
                'message': 'Invalid email',
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = random.Random().randint(111111, 999999)
            user = User.objects.get(email=request.GET.get('email'))
            send_mail(
                'Reset Password',
                f'Your confirmation code is {token}',
                'mateus@horizon-development.com',
                [user.email],
                fail_silently=False,
            )
            token = hashlib.sha256(str(self.token).encode('utf-8')).hexdigest()
            user.email_token = token
            user.email_datetime_validator = dt.now() + td(minutes=10)
            user.save()
            return Response({
                'message': 'Email sent successfully',   
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'message': 'Error sending email',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    
    #edit the params to the schema  
    @swagger_auto_schema(
        operation_summary="Reset password (Auth Not Required)",
        operation_description="Verify the token sent before with a get request to reset password. The token is valid for 10 minutes",
        operation_id="reset_password",
        tags=['Accounts Utils'],
        responses={
            200: 'New password sent to email successfully',
            400: 'Error sending email',
            401: 'Invalid token',
            403: 'Token expired',
            404: 'Missing email or token',
            417: 'User not found'
        },
        request_body=ResetPasswordWithTokenSerializer
    )
    def put(self, request, *args, **kwargs):
        email = request.data.get('email')
        token = request.data.get('token')
        if not email or not token:
            return Response({
                'message': 'Missing email or token',
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not User.objects.filter(email=email).exists():
            return Response({
                'message': 'User not found',
            }, status=status.HTTP_417_EXPECTATION_FAILED)

        
        user = User.objects.get(email=email)
        token = hashlib.sha256(str(token).encode('utf-8')).hexdigest()
        if user.email_token == token and user.email_datetime_validator > dt.now():
            try:
                #generate a random password and send it to the user
                letters = string.ascii_lowercase
                result_str = ''.join(random.choice(letters) for i in range(16))
                user.set_password(result_str)
                user.save()
                send_mail(
                    'Reset your password',
                    f'Your new password is {result_str}',
                    'mateus@horizon-development.com',
                    [user.email],
                    fail_silently=False,
                )
                return Response({
                    'message': 'Password reset successfully',
                }, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({
                    'message': 'User does not exist',
                }, status=status.HTTP_404_NOT_FOUND)
            except:
                return Response({
                    'message': 'Something went wrong',
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'message': 'Invalid token',
            }, status=status.HTTP_401_UNAUTHORIZED)



class ChangePasswordView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ChangePasswordSerializer

    @swagger_auto_schema(
        operation_summary="Change password (Auth Required)",
        operation_description="Change user password using post request",
        operation_id="change_password",
        tags=['Accounts Utils'],
        responses={
            200: 'Password changed successfully',
            400: "Password didn't match",
            401: 'Invalid password',
        },
        request_body=ChangePasswordSerializer

    )
    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        if not user.check_password(serializer.data.get("old_password")):
            return Response({
                'message': 'Invalid password',
            }, status=status.HTTP_401_UNAUTHORIZED)

        if not user.email_confirmed:
            return Response({
                'message': 'Email not confirmed',
            }, status=status.HTTP_401_UNAUTHORIZED)

        if serializer.data.get("new_password") != serializer.data.get("confirm_password"):
            return Response({
                'message': "Password didn't match",
            }, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.data.get("new_password"))
        user.save()
        return Response({
            'message': 'Password changed successfully',
        }, status=status.HTTP_200_OK)



class EditProfileView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = EditProfileSerializer
    
    @swagger_auto_schema(
        operation_summary = "Edit Profile (Auth Required)",
        operation_description = "Edit user profile using post request (Login required)",
        operation_id = "edit_profile",
        tags=['Accounts Utils'],
        responses = {
            200: 'Profile edited successfully',
            400: 'Error editing profile',
            404: 'User not found'
        },
        request_body=EditProfileSerializer
    )
    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.update(user, serializer.validated_data)
            return Response({
                'message': 'User updated successfully',
                'user': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'message': 'Something went wrong',
        }, status=status.HTTP_400_BAD_REQUEST)
            


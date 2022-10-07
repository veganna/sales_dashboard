from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken, AuthenticationFailed
from ecommerce_simple.member import MemberCore
from ecommerce_simple.models import Membership
from ecommerce_simple.serializers import MembershipSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    is_member = serializers.SerializerMethodField()
    membership = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'description','is_member', 'membership')

    def get_is_member(self, obj):
        return MemberCore(obj).is_member()

    def get_membership(self, obj):
        return MembershipSerializer(MemberCore(obj).membership, many=False).data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'password2', 'phone')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['email'],
            validated_data['first_name'],
            validated_data['last_name'],
            validated_data['phone'],
            validated_data['password'],
        )
        return user

    def save(self, **kwargs):
        user = super().save(**kwargs)
        return user

class ConfirmEmailSerializer(serializers.Serializer):
    token = serializers.CharField()

class TokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['phone'] = user.phone
        return token

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordWithTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()

class EditProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone')

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance

class ConfirmPhoneSerializer(serializers.Serializer):
    phone = serializers.CharField()
    token = serializers.CharField()

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    new_password2 = serializers.CharField()

class LoginResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    user = UserSerializer()

    





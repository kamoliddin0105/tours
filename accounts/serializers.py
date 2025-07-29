from django.db import models
from rest_framework import serializers

from accounts.models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'gmail', 'phone_number', 'password', 'username')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            gmail=validated_data['gmail'],
            phone_number=validated_data['phone_number'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username_or_phone = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        identifier = data['username_or_phone']
        password = data['password']

        user = User.objects.filter(
            models.Q(phone_number=identifier) | models.Q(username=identifier)
        ).first()

        if user and user.check_password(password):
            return user
        raise serializers.ValidationError("Telefon raqam yoki parol noto'g'ri")


class ForgotPasswordSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField()


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=6)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'gmail', 'phone_number', 'username', 'is_active', 'is_admin']

# serializers.py
from django.core.validators import validate_email
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'number', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'number': {'required': True}
        }

    def validate(self, data):
        if not data.get('email') and not data.get('number'):
            raise ValidationError("Укажите email или номер телефона")
        return data

    def validate_email(self, value):
        if value:
            try:
                validate_email(value)
            except ValidationError:
                raise serializers.ValidationError("Некорректный email адрес")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
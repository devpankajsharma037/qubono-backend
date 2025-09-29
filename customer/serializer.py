import profile
from typing import Required
from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password,check_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    password    = serializers.CharField(required=True)
    first_name  = serializers.CharField(required=False)
    last_name   = serializers.CharField(required=False,allow_null=True, allow_blank=True)
    email       = serializers.CharField(required=True,validators=[UniqueValidator(queryset=User.objects.all(),message='Email already exists')])
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        validated_data['is_active'] = True
        return super().create(validated_data)
    
    class Meta:
        model = User
        fields = ('id', 'email','password','first_name','last_name',)
        extra_kwargs = {
            'password': {
                'required': True
            },
            'email': {
                'required': True
            },
            'first_name': {
                'required': False
            },
            'last_name': {
                'required': False
            }
        }
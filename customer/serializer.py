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
        validated_data['password']  = make_password(validated_data.get('password'))
        validated_data['is_active'] = True
        validated_data['role']      = 'EMPLOYEE'
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

class UserLoginSerializer(serializers.Serializer):
    email       = serializers.EmailField(required=True)
    password    = serializers.CharField(required=True,write_only=True)
    class Meta:
        model = User
        fields = "__all__"

    def validate(self, data):
        email       = data.get('email')
        password    = data.get('password')
        if email and password:
            modelClass = self.Meta.model

            userObj = modelClass.objects.filter(email=email,is_active=False)
            if userObj.exists():
                raise serializers.ValidationError({'error':'Account is not verified'})

            userObj = modelClass.objects.filter(email=email)
            if not userObj.exists():
                raise serializers.ValidationError({'error':'Invalid credentials'})
            
            savedPasswordHash = userObj.first().password
            if not check_password(password,savedPasswordHash):
                raise serializers.ValidationError({'error':'Invalid credentials'})
            
            data['user'] = userObj.first()
        else:
            raise serializers.ValidationError({'error':'Must include "email" and "password"'})
        return data
  
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password','is_staff','is_superuser','user_permissions','groups')

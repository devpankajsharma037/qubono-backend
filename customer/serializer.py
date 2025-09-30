from rest_framework import serializers
from .models import User,Token
from rest_framework.validators import UniqueValidator
from core.utils.common import generateToken
from django.contrib.auth.hashers import make_password,check_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    password    = serializers.CharField(required=True)
    first_name  = serializers.CharField(required=False)
    last_name   = serializers.CharField(required=False,allow_null=True, allow_blank=True)
    email       = serializers.CharField(required=True,validators=[UniqueValidator(queryset=User.objects.all(),message='Email already exists')])
    
    def create(self, validated_data):
        validated_data['role']      = 'EMPLOYEE'
        validated_data['password']  = make_password(validated_data.get('password'))
        validated_data['is_active'] = False
        validated_data['username']  = validated_data.get('email')
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

class ForgotAccountValidationSerializer(serializers.Serializer):
    email    = serializers.CharField(required=True)
    def validate(self, attrs):
        email = attrs.get('email')
        try:
            try:
                userObj = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError({"email": "Account not found"}) 

            if not userObj.is_active:
                raise serializers.ValidationError({"email": "Account not activated"}) 
            
            token = generateToken(userObj)
            Token.objects.create(user=userObj,type='FORGOT_PASSWORD',token=token)
            attrs['user'] = userObj
            attrs['token'] = token
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "Email is required"}) 
        return attrs
    
class ResetPasswordSerializer(serializers.Serializer):
    password    = serializers.CharField(required=True)
    token       = serializers.CharField(required=True)
    def validate(self, attrs):
        token       = attrs.get('token')
        password    = attrs.get('password')
        try:
            tokenObj            = Token.objects.get(token=token,type='FORGOT_PASSWORD')
            userObj             = User.objects.get(email=tokenObj.user.email)
            userObj.password    = make_password(password)
            tokenObj.delete()
            attrs['user'] = userObj
        except Token.DoesNotExist:
            raise serializers.ValidationError({"token": "token is expired"}) 
        return attrs
    
class VerifyAccountSerializer(serializers.Serializer):
    token    = serializers.CharField(required=True)
    email    = serializers.CharField(required=True)
    def validate(self, attrs):
        token = attrs.get('token')
        try:
            try:
                tokenObj = Token.objects.get(token=token,type='VERFIY_ACCOUNT')
            except Token.DoesNotExist:
                raise serializers.ValidationError({"error": "token expired or not validate."})    

            try:
                userObj = User.objects.get(email=tokenObj.user.email)
            except User.DoesNotExist:
                raise serializers.ValidationError({"error": "token expired or not validate."})  
            
            tokenObj.delete()
            userObj.is_active = True
            userObj.save()
            attrs['user'] = userObj
        except User.DoesNotExist:
            raise serializers.ValidationError({"error": "token expired or not validate."})       
        return attrs
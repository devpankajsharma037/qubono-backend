from .serializer import *
from .models import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .function.jwtToken import jwtToken
from django.utils import timezone
from django.conf import settings
from core.utils.common import generateToken
from .email.authEmailSender import verificationEmail,forgotEmail
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from core.utils.scheduler import scheduler
WEB_APP_URL        = settings.WEB_APP_URL


class UserAuthView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def register(self, request):
        context = {}
        try:
            payLoad = request.data
            serializer = UserRegistrationSerializer(data=payLoad)
            if not serializer.is_valid():
                context["status"]       = False
                context["code"]         = status.HTTP_400_BAD_REQUEST
                context["message"]      = serializer.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            
            user = serializer.save()

            token = generateToken(user)
            try:
                tokenObj = Token.objects
                tokenObj.filter(user=user,type='VERFIY_ACCOUNT').delete()
                tokenObj.create(user=user,type='VERFIY_ACCOUNT',token=token)
            except:
                pass
            
            userEmail       = user.email
            emailContext    = {
                "email":userEmail,
                "url":f'{WEB_APP_URL}/verify-email?token={token}&email={userEmail}'
            }
            scheduler.add_job(verificationEmail,'date',run_date=timezone.now(), args=[emailContext])
           
            context["status"]       = True
            context["code"]         = status.HTTP_200_OK
            context["message"]      = "success"
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["status"]   = False
            context["code"]     = status.HTTP_500_INTERNAL_SERVER_ERROR
            context["message"]  = "Something went wrong please try agin later!"
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def verfiyAccount(self,request):
        context = {}
        try:
            payload             = request.data
            serializer          = VerifyAccountSerializer(data=payload)
            if not serializer.is_valid():
                context["status"]   = False
                context["code"]     = status.HTTP_400_BAD_REQUEST
                context["message"]  = serializer.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            
            user        = serializer.validated_data.get('user')
            serializer  = UserInfoSerializer(user)
            tokens      = jwtToken(user)
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            context['data']     = {
                "info": serializer.data,
                "token":{
                    "refresh": tokens["refresh"],
                    "access": tokens["access"],
                }
            }
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["status"]   = False
            context["code"]     = status.HTTP_500_INTERNAL_SERVER_ERROR
            context["message"]  = "Something went wrong please try agin later!"
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def login(self, request):
        context = {}
        try:
            serializer = UserLoginSerializer(data=request.data)
            
            if not serializer.is_valid():
                context["status"]       = False
                context["code"]         = status.HTTP_400_BAD_REQUEST
                context["message"]      = serializer.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.validated_data.get('user')
            serializer = UserInfoSerializer(user)
            tokens = jwtToken(user)

            context["status"] = True
            context["code"] = status.HTTP_200_OK
            context["message"] = "success"
            context['data'] = {
                "info": serializer.data,
                "token":{
                    "refresh": tokens["refresh"],
                    "access": tokens["access"],
                }
            }
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["status"]   = False
            context["code"]     = status.HTTP_500_INTERNAL_SERVER_ERROR
            context["message"]  = "Something went wrong please try agin later!"
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def forgotPassword(self, request):
        context = {}
        try:
            serializer = ForgotAccountValidationSerializer(data=request.data)
            if not serializer.is_valid():
                context["status"]       = False
                context["code"]         = status.HTTP_400_BAD_REQUEST
                context["message"]      = serializer.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            
            user    = serializer.validated_data.get('user')
            token   = serializer.validated_data.get('token')
            
            emailContext = {"email":user.email,"url":f'{WEB_APP_URL}/reset-password/?token={token}'}
            scheduler.add_job(forgotEmail,'date',run_date=timezone.now(), args=[emailContext])
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["status"]       = False
            context["code"]         = status.HTTP_500_INTERNAL_SERVER_ERROR
            context["message"]      = "Something went wrong please try agin later!"
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def restPassword(self, request):
        context = {}
        try:
            serializer = ResetPasswordSerializer(data=request.data)
            if not serializer.is_valid():
                context["status"]   = False
                context["code"]     = status.HTTP_400_BAD_REQUEST
                context["message"]  = serializer.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.validated_data.get('user')
            tokens = jwtToken(user)

            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            context['data'] = {
                "access": tokens["access"],
                "refresh": tokens["refresh"]
            }
            return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            context["status"] = False
            context["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            context["message"] = "Something went wrong please try agin later!"
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ProfileView(viewsets.ViewSet):
    authentication_classes  = [JWTAuthentication]
    permission_classes      = [IsAuthenticated]

    def getProfile(self,request):
        context = {}
        try:
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["status"]   = False
            context["code"]     = status.HTTP_500_INTERNAL_SERVER_ERROR
            context["message"]  = "Something went wrong please try agin later!"
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

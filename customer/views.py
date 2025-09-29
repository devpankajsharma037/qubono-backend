from .serializer import *
from .models import *
from rest_framework import viewsets, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.permissions import AllowAny



class UserRegistrationView(viewsets.ViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        context = {}
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                context["status"]       = False
                context["code"]  = status.HTTP_400_BAD_REQUEST
                context["message"]      = serializer.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
           
            context["status"]       = True
            context["code"]         = status.HTTP_200_OK
            context["message"]      = "success"
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["status"]   = False
            context["code"]     = status.HTTP_500_INTERNAL_SERVER_ERROR
            context["message"]  = "Something went wrong"
            context["error"]    = str(e)
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
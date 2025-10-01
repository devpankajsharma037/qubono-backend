from .serializer import *
from .models import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from core.utils.decorator import checkRole


class StoreAdminView(viewsets.ViewSet):
    authentication_classes  = [JWTAuthentication]
    permission_classes      = [IsAuthenticated]

    @checkRole()
    def createStore(self,request):
        context = {}
        try:
            payLoad     = request.data
            serializer  = StoreSerializer(data=payLoad,context={"request":request})
            if not serializer.is_valid():
                context["status"]   = False
                context["code"]     = status.HTTP_400_BAD_REQUEST
                context["message"]  = serializer.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["status"]   = False
            context["code"]     = status.HTTP_500_INTERNAL_SERVER_ERROR
            context["message"]  = "Something went wrong please try agin later!"
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @checkRole()
    def storeList(self,request):
        context = {}
        try:
            userObj             = request.user
            storeQueryObj       = Store.objects.filter(user=userObj)
            serializer          = StoreListSerializer(storeQueryObj,many=True)
            context["data"]     = serializer.data
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            context["status"]   = False
            context["code"]     = status.HTTP_500_INTERNAL_SERVER_ERROR
            context["message"]  = "Something went wrong please try agin later!"
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @checkRole()
    def storeBySlug(self,request,slug):
        context = {}
        try:
            userObj             = request.user
            try:
                storeQueryObj   = Store.objects.get(user=userObj,slug=slug)
            except Store.DoesNotExist as e:
                context["status"]   = False
                context["code"]     = status.HTTP_400_BAD_REQUEST
                context["message"]  = "Store not found!"
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
            serializer          = StoreListSerializer(storeQueryObj)
            context["data"]     = serializer.data
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["status"]   = False
            context["code"]     = status.HTTP_500_INTERNAL_SERVER_ERROR
            context["message"]  = "Something went wrong please try agin later!"
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @checkRole()
    def deleteStore(self,request,slug):
        context = {}
        try:
            userObj             = request.user
            try:
                storeQueryObj   = Store.objects.get(user=userObj,slug=slug)
            except Store.DoesNotExist as e:
                context["status"]   = False
                context["code"]     = status.HTTP_400_BAD_REQUEST
                context["message"]  = "Store not found!"
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
            storeQueryObj.delete()
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["status"]   = False
            context["code"]     = status.HTTP_500_INTERNAL_SERVER_ERROR
            context["message"]  = "Something went wrong please try agin later!"
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @checkRole()
    def updateStore(self,request):
        context = {}
        try:
            payLoad     = request.data
            userObj     = request.user
            serializer  = StoreUpdateValidationSerializer(data=payLoad)
            if not serializer.is_valid():
                context["status"]   = False
                context["code"]     = status.HTTP_400_BAD_REQUEST
                context["message"]  = serializer.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
                
            try:
                storeObj   = Store.objects.get(user=userObj,id=payLoad['id'])
            except Store.DoesNotExist as e:
                context["status"]   = False
                context["code"]     = status.HTTP_400_BAD_REQUEST
                context["message"]  = "Store not found!"
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            
            serializer  = StoreUpdateSerializer(storeObj,data=payLoad,partial=True)
            if not serializer.is_valid():
                context["status"]   = False
                context["code"]     = status.HTTP_400_BAD_REQUEST
                context["message"]  = serializer.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            context["status"]   = False
            context["code"]     = status.HTTP_500_INTERNAL_SERVER_ERROR
            context["message"]  = "Something went wrong please try agin later!"
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
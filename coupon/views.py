from .serializer import *
from .models import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from core.utils.decorator import checkRole,checkAccountStatus
from django.db.models import Q

# Admin View
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
            categories    = request.query_params.getlist('category')
            subCategories = request.query_params.getlist('sub_category')
            filters = Q()
            optional_filter = Q()
            if subCategories:
                optional_filter &= Q(sub_category__in=subCategories)
            if categories:
                optional_filter |= Q(sub_category__category__in=categories)

            if optional_filter:
                filters &= optional_filter

            storeQueryObj = Store.objects.filter(filters).distinct()
            serializer          = StoreListSerializer(storeQueryObj,many=True)
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
        
            serializer          = StoreListWithCouponSerializer(storeQueryObj,context={"store": storeQueryObj, "request": request})
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
            context["status"]   = False
            context["code"]     = status.HTTP_500_INTERNAL_SERVER_ERROR
            context["message"]  = "Something went wrong please try agin later!"
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @checkRole()
    def storeCouponByFllter(self,request):
        context = {}
        try:
            payLoad       = request.data
            userObj       = request.user
            categories    = payLoad.get('category', None)
            subCategories = payLoad.get('sub_category', None)
            store         = payLoad.get('store', None)
            couponType    = payLoad.get('type', "ALL")

            filters         = Q(user=userObj)
            optional_filter = Q()
            
            if subCategories:
                optional_filter &= Q(sub_category__in=subCategories)

            if categories:
                optional_filter |= Q(sub_category__category__in=categories)

            if optional_filter:
                filters &= optional_filter

            if couponType and couponType != "ALL":
                filters &= Q(type=couponType)
            
            if store:
                filters &= Q(store=store)

            storeQueryObj       = Coupon.objects.filter(filters).distinct()
            serializer          = StoreCouponSerializer(storeQueryObj, many=True)
            context["data"]     = serializer.data
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["data"]     = []
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            context["error"]    = str(e)
            return Response(context, status=status.HTTP_200_OK)

class CategoryAdminView(viewsets.ViewSet):
    authentication_classes  = [JWTAuthentication]
    permission_classes      = [IsAuthenticated]

    @checkRole()
    def categoryListByFilter(self,request):
        context = {}
        try:
            categoryQuerySets   = Category.objects.all()
            serializer          = CategorySerializer(categoryQuerySets,many=True)
            context['data']     = serializer.data
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["data"]     = []
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @checkRole()
    def categoryCreate(self,request):
        context = {}
        try:
            payLoad         = request.data
            payLoad['user'] = request.user.id
            payLoad['is_active']    = True
            serializer  = CategoryValidateSerializer(data=payLoad,context={'request':request})
            if not serializer.is_valid():
                context["status"]   = False
                context["code"]     = status.HTTP_400_BAD_REQUEST
                context["message"]  = serializer.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            category_data = serializer.save()
            context['data']       = CategorySerializer(category_data).data
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            context["status"]   = False
            context["code"]     = status.HTTP_500_INTERNAL_SERVER_ERROR
            context["message"]  = str(e)
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @checkRole()
    def categoryUpdate(self,request):
        context = {}
        try:
            payLoad     = request.data
            categoryId  = payLoad.get("id")

            if not categoryId:
                context["status"] = False
                context["code"] = status.HTTP_400_BAD_REQUEST
                context["message"] = "Category ID is required in the payload."
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            try:
                category = Category.objects.get(pk=categoryId)
            except Category.DoesNotExist:
                context["status"]   = False
                context["code"]     = status.HTTP_404_NOT_FOUND
                context["message"]  = "Category not found."
                return Response(context, status=status.HTTP_404_NOT_FOUND)
        
            serializer = CategoryValidateSerializer(category,data=payLoad,partial=True)
            if not serializer.is_valid():
                context["status"]   = False
                context["code"]     = status.HTTP_400_BAD_REQUEST
                context["error"]    = serializer.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            category_data=serializer.save()
            context['data']     = CategorySerializer(category_data).data
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            context["status"]   = False
            context["code"]     = status.HTTP_500_INTERNAL_SERVER_ERROR
            context["message"]  = str(e)
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @checkRole()
    def categoryDelete(self,request,uuid=None):
        context = {}
        try:
            try:
                category = Category.objects.get(pk=uuid)
            except Category.DoesNotExist:
                context["status"]   = False
                context["code"]     = status.HTTP_404_NOT_FOUND
                context["error"]    = "Category not found."
                return Response(context, status=status.HTTP_404_NOT_FOUND)
    
            category.delete()
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["status"]   = False
            context["code"]     = status.HTTP_500_INTERNAL_SERVER_ERROR
            context["message"]  = "Something went wrong please try agin later!"
            context["error"]    = str(e)
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @checkRole()
    def singleCategory(self,request,uuid):
        context = {}
        try:
            try:
                categoryObj = Category.objects.get(pk=uuid)
            except Category.DoesNotExist:
                context["status"]   = False
                context["code"]     = status.HTTP_404_NOT_FOUND
                context["error"]    = "Category not found."
                return Response(context, status=status.HTTP_404_NOT_FOUND)
    
            serializer          = CategorySerializer(categoryObj)
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            context["data"]     = serializer.data
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["status"]   = False
            context["code"]     = status.HTTP_500_INTERNAL_SERVER_ERROR
            context["message"]  = "Something went wrong please try agin later!"
            context["error"]    = str(e)
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserAdminView(viewsets.ViewSet):
    authentication_classes  = [JWTAuthentication]
    permission_classes      = [IsAuthenticated]

    @checkRole()
    def userListByFilter(self,request):
        context = {}
        try:
            
            isActiveUser    = request.query_params.get('is_active',None)
            userRole        = request.query_params.get('role',None)
            filters = Q()
            optional_filter = Q()
            if userRole:
                optional_filter &= Q(role=userRole)
            if isActiveUser:

                if isActiveUser == 'false':
                    isActiveUser = True
                else:
                    isActiveUser = False

                optional_filter &= Q(is_delete=isActiveUser)

            if optional_filter:
                filters &= optional_filter

            userQuerySets       = User.objects.filter(filters).distinct()
            serializer          = UserSerializer(userQuerySets,many=True)
            context['data']     = serializer.data
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["status"]   = False
            context["code"]     = status.HTTP_500_INTERNAL_SERVER_ERROR
            context["message"]  = "Something went wrong please try agin later!"
            context["error"]    = str(e)
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @checkRole()
    def updateUser(self,request):
        context = {}
        try:
            payLoad     = request.data
            serializer  = UserUpdateValidationSerializer(data=payLoad)
            if not serializer.is_valid():
                context["status"]   = False
                context["code"]     = status.HTTP_400_BAD_REQUEST
                context["message"]  = serializer.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            
            userId      = payLoad['id']

            payLoad['is_delete'] = payLoad['is_active']
            userObj     = User.objects.get(id=userId)
            serializer  = UserUpdateSerializer(userObj,data=payLoad,partial=True)
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
            context["error"]    = str(e)
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class SubCategoryAdminView(viewsets.ViewSet):
    authentication_classes  = [JWTAuthentication]
    permission_classes      = [IsAuthenticated]

    @checkRole()
    def subCategoryListByFilter(self,request):
        context = {}
        try:
            subcategoryQuerySets   = SubCategory.objects.all()
            serializer          = SubCategorySerializer(subcategoryQuerySets,many=True)
            context['data']     = serializer.data
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["data"]     = []
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @checkRole()
    def subCategoryCreate(self,request):
        context = {}
        try:
            payLoad         = request.data
            payLoad['user'] = request.user.id
            payLoad['is_active']    = True
            serializer  = SubCategoryValidateSerializer(data=payLoad,context={'request':request})
            if not serializer.is_valid():
                context["status"]   = False
                context["code"]     = status.HTTP_400_BAD_REQUEST
                context["message"]  = serializer.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            category_data = serializer.save()
            context['data']       = SubCategorySerializer(category_data).data
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            context["status"]   = False
            context["code"]     = status.HTTP_500_INTERNAL_SERVER_ERROR
            context["message"]  = str(e)
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @checkRole()
    def subCategoryUpdate(self,request):
        context = {}
        try:
            payLoad     = request.data
            subcategoryId  = payLoad.get("id")

            if not subcategoryId:
                context["status"] = False
                context["code"] = status.HTTP_400_BAD_REQUEST
                context["message"] = "Subcategory ID is required in the payload."
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            try:
                subcategory = SubCategory.objects.get(pk=subcategoryId)
            except Category.DoesNotExist:
                context["status"]   = False
                context["code"]     = status.HTTP_404_NOT_FOUND
                context["message"]  = "Subcategory not found."
                return Response(context, status=status.HTTP_404_NOT_FOUND)
        
            serializer = SubCategoryValidateSerializer(subcategory,data=payLoad,partial=True)
            if not serializer.is_valid():
                context["status"]   = False
                context["code"]     = status.HTTP_400_BAD_REQUEST
                context["error"]    = serializer.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            subcategory_data=serializer.save()
            context['data']     = CategorySerializer(category_data).data
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            context["status"]   = False
            context["code"]     = status.HTTP_500_INTERNAL_SERVER_ERROR
            context["message"]  = str(e)
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @checkRole()
    def subCategoryDelete(self,request,uuid=None):
        context = {}
        try:
            try:
                subcategory = SubCategory.objects.get(pk=uuid)
            except SubCategory.DoesNotExist:
                context["status"]   = False
                context["code"]     = status.HTTP_404_NOT_FOUND
                context["error"]    = "Sub-Category not found."
                return Response(context, status=status.HTTP_404_NOT_FOUND)
    
            subcategory.delete()
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["status"]   = False
            context["code"]     = status.HTTP_500_INTERNAL_SERVER_ERROR
            context["message"]  = "Something went wrong please try agin later!"
            context["error"]    = str(e)
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @checkRole()
    def singleCategory(self,request,uuid):
        context = {}
        try:
            try:
                subcategoryObj = SubCategory.objects.get(pk=uuid)
            except SubCategory.DoesNotExist:
                context["status"]   = False
                context["code"]     = status.HTTP_404_NOT_FOUND
                context["error"]    = "sub-Category not found."
                return Response(context, status=status.HTTP_404_NOT_FOUND)
    
            serializer          = SubCategorySerializer(subcategoryObj)
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            context["data"]     = serializer.data
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["status"]   = False
            context["code"]     = status.HTTP_500_INTERNAL_SERVER_ERROR
            context["message"]  = "Something went wrong please try agin later!"
            context["error"]    = str(e)
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# User Public View
class StoreUserView(viewsets.ViewSet):
    def storeList(self, request):
        context = {}
        try:
            categories    = request.query_params.getlist('category')
            subCategories = request.query_params.getlist('sub_category')


            filters = Q(is_active=True, is_deleted=False)

            optional_filter = Q()
            if subCategories:
                optional_filter &= Q(sub_category__in=subCategories)
            if categories:
                optional_filter |= Q(sub_category__category__in=categories)

            if optional_filter:
                filters &= optional_filter

            storeQueryObj = Store.objects.filter(filters).distinct()

            serializer = StoreListSerializer(storeQueryObj, many=True)
            context["data"]     = serializer.data
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            print(str(e))
            context["data"]     = []
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            return Response(context, status=status.HTTP_200_OK)
    
    def storeBySlug(self,request,slug):
        context = {}
        try:
            try:
                storeQueryObj   = Store.objects.get(slug=slug,is_active=True,is_deleted=False)
            except Store.DoesNotExist as e:
                context["status"]   = False
                context["code"]     = status.HTTP_400_BAD_REQUEST
                context["message"]  = "Store not found!"
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
            serializer          = StoreListWithCouponSerializer(storeQueryObj,context={"store": storeQueryObj, "request": request})
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

    def storeCouponByFllter(self,request):
        context = {}
        try:
            payLoad       = request.data
            
            categories    = payLoad.get('category', None)
            subCategories = payLoad.get('sub_category', None)
            store         = payLoad.get('store', None)
            couponType    = payLoad.get('type', "ALL")

            filters = Q(is_active=True, is_deleted=False)

            optional_filter = Q()

            if subCategories:
                optional_filter &= Q(sub_category__in=subCategories)

            if categories:
                optional_filter |= Q(sub_category__category__in=categories)

            if optional_filter:
                filters &= optional_filter

            if couponType and couponType != "ALL":
                filters &= Q(type=couponType)
            
            if store:
                filters &= Q(store=store)

            storeQueryObj = Coupon.objects.filter(filters).distinct()
            serializer = StoreCouponSerializer(storeQueryObj, many=True)
            context["data"]     = serializer.data
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["data"]     = []
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            context["error"]    = str(e)
            return Response(context, status=status.HTTP_200_OK)

class CategoryView(viewsets.ViewSet):
    serializer_class        = CategorySerializer

    def categoryListByFilter(self,request):
        context = {}
        try:
            categoryQuerySets   = Category.objects.filter(is_active=True,is_deleted=False)
            serializer          = self.serializer_class(categoryQuerySets,many=True)
            context['data']     = serializer.data
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["data"]     = []
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RatingView(viewsets.ViewSet):
    serializer_class        = RatingSerializer

    def ratingListView(self,request):
        context = {}
        try:
            payLoad             = request.data
            serializer          = RatingListValidationSerializer(data=payLoad)
            if not serializer.is_valid():
                context["status"]   = False
                context["code"]     = status.HTTP_400_BAD_REQUEST
                context["message"]  = serializer.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            
            storeId             = payLoad['store']
            ratingQuerySets     = Rating.objects.filter(store=storeId,is_approved=True,is_active=True,is_deleted=False)
            serializer          = self.serializer_class(ratingQuerySets,many=True)
            context['data']     = serializer.data
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["data"]     = []
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# User Logged View
class WishListLoggedView(viewsets.ViewSet):
    authentication_classes  = [JWTAuthentication]
    permission_classes      = [IsAuthenticated]
    serializer_class        = WishlistSerializer
    
    @checkAccountStatus()
    def wishListCreateRemove(self,request):
        context = {}
        try:
            payLoad                 = request.data
            userObj                 = request.user
            payLoad['user']         = userObj.id
            payLoad['is_active']    = True
            serializer = WishlistValidationSerializer(data=payLoad)
            if not serializer.is_valid():
                context["status"]       = False
                context["code"]         = status.HTTP_400_BAD_REQUEST
                context["message"]      = serializer.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            storeId = payLoad['store_id']
            try:
                Wishlist.objects.get(user=userObj,store=storeId).delete()
            except:
                payLoad['store'] = storeId
                serializer = self.serializer_class(data=payLoad)
                if not serializer.is_valid():
                    context["status"]       = False
                    context["code"]         = status.HTTP_400_BAD_REQUEST
                    context["message"]      = serializer.errors
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

    @checkAccountStatus()
    def wishList(self,request):
        context = {}
        try:
            userObj     = request.user
            wishListQuerySets   = Wishlist.objects.filter(user=userObj)
            serializer          = self.serializer_class(wishListQuerySets,many=True)
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
        
class RatingLoggedView(viewsets.ViewSet):
    authentication_classes  = [JWTAuthentication]
    permission_classes      = [IsAuthenticated]
    serializer_class        = RatingCreateSerializer

    @checkAccountStatus()
    def ratingCreate(self,request):
        context = {}
        try:
            payLoad                 = request.data
            userObj                 = request.user
            payLoad['user']         = userObj.id
            payLoad['is_active']    =  True
            serializer  = RatingCreateValidationSerializer(data=payLoad,context={"user":userObj})
            if not serializer.is_valid():
                context["status"]       = False
                context["code"]         = status.HTTP_400_BAD_REQUEST
                context["message"]      = serializer.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = self.serializer_class(data=payLoad)

            if not serializer.is_valid():
                context["status"]       = False
                context["code"]         = status.HTTP_400_BAD_REQUEST
                context["message"]      = serializer.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["data"]     = []
            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["message"]  = "success"
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
from rest_framework import serializers
from .models import (Store,SubCategory,Category,Coupon,CouponType,Wishlist)

class StoreSerializer(serializers.ModelSerializer):
    name        = serializers.CharField(required=True)
    logo        = serializers.ImageField(required=True)
    category    = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, required=True)
    sub_category = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all(), many=True, required=True)

    class Meta:
        model = Store
        fields = "__all__"
        read_only_fields = ["user"]     

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data['is_active'] = True
        validated_data["user"] = request.user
        categories = validated_data.pop("category", [])
        sub_categories = validated_data.pop("sub_category", [])
        store = super().create(validated_data)
        store.category.set(categories)
        store.sub_category.set(sub_categories)
        return store

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    sub_categorys = SubCategorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = "__all__"

class StoreListSerializer(serializers.ModelSerializer):
    # category    = CategorySerializer(many=True)
    offers      = serializers.SerializerMethodField() 
    class Meta:
        model = Store
        exclude  = ("user","sub_category",)
        read_only_fields = ["user"]

    def get_offers(self, obj):
        return [
            {
                "count":obj.coupons.count(),
                "name":"offers",
            },
        ]

class StoreUpdateValidationSerializer(serializers.Serializer):
    id          = serializers.UUIDField(required=True)
    name        = serializers.CharField(required=True)
    category    = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, required=True)
    sub_category = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all(), many=True, required=True)

    def validate(self, attrs):
        categories = attrs.get('category', [])
        if not categories or len(categories) == 0:
            raise serializers.ValidationError({
                'category': 'At least one category is required.'
            })
        
        sub_categories = attrs.get('sub_category', [])
        if not sub_categories or len(sub_categories) == 0:
            raise serializers.ValidationError({
                'sub_category': 'At least one sub-category is required.'
            })
        return super().validate(attrs)

class StoreUpdateSerializer(serializers.ModelSerializer):
    id          = serializers.UUIDField(required=True)
    name        = serializers.CharField(required=True)
    category    = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, required=True)
    sub_category = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all(), many=True, required=True)

    class Meta:
        model = Store
        fields = "__all__" 

class StoreCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        exclude  = ("code","sub_category","store","user",)

class SubCategoryWithCouponSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    class Meta:
        model = SubCategory
        exclude = ("category","user")

    def get_count(self, obj):
        store = self.context.get("store")
        if not store:
            return 0
        return obj.coupon_set.filter(store=store).count()
    
class CategoryWithCouponSerializer(serializers.ModelSerializer):
    sub_categorys   = serializers.SerializerMethodField()
    count           = serializers.SerializerMethodField()
    class Meta:
        model = Category
        exclude = ("user",)

    def get_sub_categorys(self, obj):
        store = self.context.get("store")
        if not store:
            return []
        subcats = SubCategory.objects.filter(category=obj,coupon__store=store).distinct()
        return SubCategoryWithCouponSerializer(subcats, many=True, context={"store": store}).data

    def get_count(self, obj):
        store = self.context.get("store")
        if not store:
            return 0
        return Coupon.objects.filter(store=store, sub_category__category=obj).count()
    
class StoreListWithCouponSerializer(serializers.ModelSerializer):
    categories  = serializers.SerializerMethodField()
    all         = StoreCouponSerializer(many=True, source='coupons')
    counts      = serializers.SerializerMethodField() 
    
    class Meta:
        model = Store
        exclude = ("user","category","sub_category",)

    def get_categories(self, obj):
        categories = Category.objects.filter(sub_categorys__coupon__store=obj).distinct()
        return CategoryWithCouponSerializer(categories, many=True, context={"store": obj}).data

    def get_counts(self, obj):
        return [
            {
                "count":obj.coupons.filter(type=CouponType.DEAL).count(),
                "name":"Deals",
                "filter_value":CouponType.DEAL,
            },
            {
                "count":obj.coupons.filter(type=CouponType.COUPON).count(),
                "name":"coupons",
                "filter_value":CouponType.COUPON,
            },
            {
                "count":obj.coupons.filter(type=CouponType.GIFT_CARD).count(),
                "name":"Gift cards",
                "filter_value":CouponType.GIFT_CARD,
            },
            {
                "count":obj.coupons.filter(type=CouponType.CASHBACK).count(),
                "name":"Cash backs",
                "filter_value":CouponType.CASHBACK,
            },
            {
                "count":obj.coupons.count(),
                "name":"all",
                "filter_value":"ALL",
            },
        ]
    
class WishlistValidationSerializer(serializers.Serializer):
    store_id = serializers.CharField(required=True)

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = "__all__"
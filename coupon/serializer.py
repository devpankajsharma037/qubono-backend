from rest_framework import serializers
from .models import Store,SubCategory,Category

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

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class SubCategorySerializer(serializers.ModelSerializer):
    category        = CategorySerializer()
    class Meta:
        model = SubCategory
        fields = "__all__"

class StoreListSerializer(serializers.ModelSerializer):
    category        = CategorySerializer(many=True)
    sub_category    = SubCategorySerializer(many=True)

    class Meta:
        model = Store
        exclude  = ("user",)
        read_only_fields = ["user"]

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
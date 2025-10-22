from rest_framework import serializers
from .models import *
from coupon.serializer import OrderCouponSerializer

class PaymentValidateSerializer(serializers.Serializer):
    coupon_id               = serializers.CharField(required=True)
    discount_applied        = serializers.BooleanField(required=True)

    def validate(self,attrs):
        coupon_id = attrs.get('coupon_id')
        try:
            coupon = Coupon.objects.get(id=coupon_id,is_active=True)
        except:
            raise serializers.ValidationError({
                'error': 'Not found'
            })

        if coupon.available_stock <= 0:
            raise serializers.ValidationError({
                'error': "No longer available or has reached its usage limit."
            })

        if coupon.validate_till < timezone.now():
            raise serializers.ValidationError({
                'error': "Expired."
            })

        attrs['coupon'] = coupon
        return attrs

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
    
class OrderSerializer(serializers.ModelSerializer):
    coupon = OrderCouponSerializer()
    class Meta:
        model = Order
        fields = '__all__'

class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


    


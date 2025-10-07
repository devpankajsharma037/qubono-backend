from rest_framework import serializers
from .models import *

from customer.models import User

class PaymentValidateSerializer(serializers.Serializer):
    coupon_id               = serializers.CharField(required=True)
    discount_applied        = serializers.BooleanField(required=True)

    def validate(self,attrs):
        coupon_id = attrs.get('coupon_id')
        try:
            coupon = Coupon.objects.get(id=attrs['coupon_id'],)
        except:
            raise serializers.ValidationError({
                'error': 'coupon not found'
            })

        attrs['coupon'] = coupon
        return attrs

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
    




    


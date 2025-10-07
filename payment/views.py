from .models import *
from .serializer import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
import razorpay
from django.utils import timezone
import os

client = razorpay.Client(auth=(os.getenv("key_id"), os.getenv("key_secret")))


class PaymentViewset(viewsets.ViewSet):
    authentication_classes  = [JWTAuthentication]
    permission_classes      = [IsAuthenticated]

    def createOrder(self,request):
        context = {}
        try:
            payload = request.data
            userId  = request.user.id
            serializer  = PaymentValidateSerializer(data=payload)
            if not serializer.is_valid():
                context["status"]   = False
                context["code"]     = status.HTTP_400_BAD_REQUEST
                context["message"]  = serializer.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            
            coupon              = serializer.validated_data['coupon']
            discount_applied    = serializer.validated_data['discount_applied']

            if coupon.available_stock <= 0:
                    context["status"] = False
                    context["code"] = status.HTTP_400_BAD_REQUEST
                    context["message"] = "This coupon is no longer available or has reached its usage limit."
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)

            if coupon.validate_till < timezone.now():
                context["status"] = False
                context["code"] = status.HTTP_400_BAD_REQUEST
                context["message"] = "This coupon has expired."
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            if discount_applied:
                if not coupon.discount:
                    final_amount = coupon.min_order_amount
                else:
                    if coupon.discount_type == 'FLAT':
                        final_amount = (coupon.min_order_amount - float(coupon.discount))
                    elif coupon.discount_type == 'PERCTANGE':
                        discount_value = (coupon.min_order_amount * float(coupon.discount)) / 100
                        final_amount = coupon.min_order_amount - discount_value       
            else:
                final_amount = coupon.min_order_amount


            context['status']       = True
            context["code"]         = status.HTTP_200_OK
            context["message"]      = "success"

            payment = {
                'price': final_amount,
                'platform_name':payload.get('platform_name','razorpay'),
                'user':userId,
                'is_active':True    
            }

            serializer = PaymentCreateSerializer(data=payment)
            if not serializer.is_valid():
                context["status"]   = False
                context["code"]     = status.HTTP_400_BAD_REQUEST
                context["message"]  = serializer.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            paymentObj = serializer.save()
            

            payment_payload = {
                "amount": final_amount*100,
                "currency": "INR",
                "receipt": "receipt#1",
                "notes": {
                    "user": str(userId),
                    "payment_id": str(paymentObj.id),
                    "coupon":str(coupon.id)
                }
            }

            data = client.order.create(data=payment_payload) 
            paymentObj.order_id =  data['id']
            paymentObj.save()

            context['status']       = True
            context["code"]         = status.HTTP_200_OK
            context["message"]      = "success"
            context["data"]         = data
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            context["status"]   = False
            context["code"]     = status.HTTP_500_INTERNAL_SERVER_ERROR
            context["message"]  = "Something went wrong please try agin later!"
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def paymentStatus(self,request):
        context ={}
        try:
            payload             = request.data
            razorpay_order_id   = payload.get("order_id")
            razorpay_payment_id = payload.get("payment_id",'')
            payment_status      = payload.get("status")
            payment = Payment.objects.get(order_id=razorpay_order_id)
            payment.status = payment_status
            payment.payment_id = razorpay_payment_id
            payment.save()

            context['code']     = 490
            if payment_status == "SUCCESS":
                 
                total_amount = payment.price
                discount_amount = 0.0
                coupon = None

            # Handle coupon
                coupon_id = payload.get("coupon_id")
                if coupon_id:
                    try:
                        coupon = Coupon.objects.get(id=coupon_id)
                        # Check minimum order amount
                        if total_amount >= coupon.min_order_amount:
                            if coupon.discount_type == 'FLAT':
                                discount_amount = coupon.discount
                            elif coupon.discount_type == 'PERCENTAGE':
                                discount_amount = (coupon.discount / 100) * total_amount
                        else:
                            coupon = None
                            discount_amount = 0.0
                    except Coupon.DoesNotExist:
                        coupon = None
                        discount_amount = 0.0

            # Ensure discount_amount does not exceed total_amount
                discount_amount = min(discount_amount, total_amount)
                final_amount = total_amount - discount_amount
                # Create Order
                order = Order.objects.create(
                        coupon=coupon,
                        payment=payment,
                        user=request.user,
                        total_amount=total_amount,
                        discount_amount=discount_amount,
                        final_amount=final_amount,
                        delivery_address=payload.get("delivery_address", ""),
                        meta={
                            "razorpay_order_id": razorpay_order_id,
                            "razorpay_payment_id": razorpay_payment_id
                        }
                )
                

                # Step 4: Record Coupon Usage
                if coupon:
                    CouponUsage.objects.create(
                        coupon=coupon,
                        user=request.user,
                        order=order,
                        meta={"used_at": timezone.now().isoformat()}
                    )

                    coupon.available_stock = max(coupon.available_stock - 1, 0)
                    coupon.save()

                    context["message"] = "Payment successful, order created"
                    context["order"] = {
                        "order_id": order.order_id,
                        "final_amount": order.final_amount,
                        "payment_id": payment.payment_id,
                        "status": payment.status
                    }

            elif payment_status.upper() == "FAILED":
                context["message"] = "Payment failed"
            else:
                context["message"] = "Payment status updated"

            context["status"] = True
            context["code"] = status.HTTP_200_OK
            return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            print(str(e))
            context["status"] = False
            context["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            context["message"] = "Something went wrong, please try again later!"
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






       








            
        


from .models import *
from .serializer import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
import razorpay
import os
from core.utils.decorator import checkAccountStatus

client = razorpay.Client(auth=(os.getenv("RAZORPAY_KEY_ID"), os.getenv("RAZORPAY_KEY_SECRET")))


class PaymentViewset(viewsets.ViewSet):
    authentication_classes  = [JWTAuthentication]
    permission_classes      = [IsAuthenticated]

    @checkAccountStatus()
    def createOrder(self,request):
        context = {}
        try:
            payload     = request.data
            userId      = request.user.id
            serializer  = PaymentValidateSerializer(data=payload)
            if not serializer.is_valid():
                context["status"]   = False
                context["code"]     = status.HTTP_400_BAD_REQUEST
                context["message"]  = serializer.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            
            coupon              = serializer.validated_data['coupon']
            discount_applied    = serializer.validated_data['discount_applied']

            if discount_applied:
                if not coupon.discount:
                    final_amount = coupon.min_order_amount
                else:
                    if coupon.discount_type == 'FLAT':
                        final_amount = (coupon.min_order_amount - float(coupon.discount))
                    elif coupon.discount_type == 'PERCENTAGE':
                        discount_value = (coupon.min_order_amount * float(coupon.discount)) / 100
                        print(discount_value)
                        final_amount = coupon.min_order_amount - discount_value       
            else:
                final_amount = coupon.min_order_amount

            payment = {
                'price': final_amount,
                'platform_name':"razorpay",
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
            context["status"]   = False
            context["code"]     = status.HTTP_500_INTERNAL_SERVER_ERROR
            context["message"]  = "Something went wrong please try agin later!"
            context["error"]    = str(e)
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @checkAccountStatus()
    def paymentStatus(self,request):
        context ={}
        try:
            payload             = request.data
            razorpay_order_id   = payload.get("order_id")
            razorpay_payment_id = payload.get("payment_id",'')
            payment_status      = payload.get("status")
            coupon_id           = payload.get("coupon_id")
    
            payment = Payment.objects.get(order_id=razorpay_order_id)
            payment.status = payment_status
            payment.payment_id = razorpay_payment_id
            payment.save()


            if payment_status == "SUCCESS":   
                
                discount_amount = 0.0

                coupon          = Coupon.objects.get(id=coupon_id)

                coupon.available_stock = max(coupon.available_stock - 1, 0)
                coupon.save()

                total_amount = final_amount   = coupon.min_order_amount
                if coupon.discount:
                    discount = float(coupon.discount)
                    if coupon.discount_type == 'FLAT':
                        discount_amount = discount
                    elif coupon.discount_type == 'PERCENTAGE':
                        discount_amount = (discount / 100) * total_amount

                    final_amount = total_amount - discount_amount
                # Create Order
                order = Order.objects.create(
                    coupon=coupon,
                    payment=payment,
                    user=request.user,
                    total_amount=total_amount,
                    discount_amount=discount_amount,
                    final_amount=final_amount,
                    is_active=True,
                    meta={
                        "razorpay_order_id": razorpay_order_id,
                        "razorpay_payment_id": razorpay_payment_id
                    }
                )
            
                if coupon:
                    CouponUsage.objects.create(coupon=coupon,user=request.user,order=order,is_active=True,)
                    
                context["code"]     = status.HTTP_200_OK
                context["message"] = "success"
            elif payment_status.upper() == "FAILED":
                context["message"]  = "Payment failed"
                context["code"]     = status.HTTP_400_BAD_REQUEST
            else:
                context['code']    = 490
                context["message"] = "Payment canceled"

            context["status"]   = True
            context["code"]     = status.HTTP_200_OK
            context["payment_status"]   = payment_status
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["status"]   = False
            context["code"]     = status.HTTP_500_INTERNAL_SERVER_ERROR
            context["message"]  = "Something went wrong, please try again later!"
            context["error"]    = str(e)
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @checkAccountStatus()
    def paymentList(self,request):
        context = {}
        try:
            userObj             = request.user
            paymentQuerySets    = Payment.objects.filter(user=userObj)
            serializer          = PaymentListSerializer(paymentQuerySets,many=True)
            context["data"]     = serializer.data
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

class UserOrderViewset(viewsets.ViewSet):
    authentication_classes  = [JWTAuthentication]
    permission_classes      = [IsAuthenticated]

    @checkAccountStatus()
    def userOrderList(self,request):
        context = {}
        try:
            userObj         = request.user
            orderQuerySets  = Order.objects.filter(user=userObj)
            serializer      = OrderSerializer(orderQuerySets,many=True)
            context["data"]     = serializer.data
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

       








            
        


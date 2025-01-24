
from rest_framework.response import Response

from base.models import  MenuItem, Order, OrderItem, DeliveryAddress, PaymentInfo
from base.serializers import OrderSerializer

from rest_framework import status
from datetime import datetime

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsEmployeeUser, IsOwnerUser
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


# add new order from authenticated user
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):

    user = request.user
    data = request.data

    orderItems = data['orderItems']

    if orderItems and len(orderItems) == 0:
        return Response({'detail': 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
        
    else:

        order = Order.objects.create(
            user = user,
            paymentMethod = data['paymentMethod'],
            vat = data['vat'],
            deliveryCharge = data['deliveryCharge'],
            totalPrice = data['totalPrice']
        )

        delivery = DeliveryAddress.objects.create(
            order=order,
            address=data['DeliveryAddress']['address'],
            city=data['DeliveryAddress']['city'],
            postalCode=data['DeliveryAddress']['postalCode'],
            country=data['DeliveryAddress']['country'],
        )

        for i in orderItems:
            item = MenuItem.objects.get(_id=i['item'])
            menu = item.menu
            restaurant = menu.restaurant

            item = OrderItem.objects.create(
                item=item,
                order=order,
                name=item.name,
                qty=i['qty'],
                price=i['price'],
                restaurant=restaurant,
            )


            item.save()

        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)
    

# view user's created orders
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
    user = request.user
    orders = user.order_set.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


# view single order
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):

    user = request.user
    try:
        order = Order.objects.get(_id=pk)

        if order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            Response({'details': 'Not authorized to view this order'}, 
                    status = status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'details': 'Order does not exist'},
                    status = status.HTTP_400_BAD_REQUEST)


# view orders for restaurant
@api_view(['GET'])
@permission_classes([IsEmployeeUser | IsOwnerUser])
def getResOrders(request):
    user_profile = request.user.userprofile
    orders = Order.objects.filter(orderitem__restaurant=user_profile.restaurant)

    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


# payment option for order
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def makePayment(request, pk):
    order = Order.objects.get(_id=pk)
    if order.isPaid == False:
        if order.user == request.user:

            amount = int(order.totalPrice)*100   # as stripe is getting the amount values in cents
            currency = 'usd'
            description = 'Test payment'

            try:
                payment_intent = stripe.PaymentIntent.create(
                    amount=amount,
                    currency=currency,
                    description=description,
                )
                amount = amount/100
                context = {
                    'client_secret': payment_intent.client_secret,
                    'amount': amount,
                    'currency': currency,
                }
                
                payment_info = PaymentInfo.objects.create(
                order=order,
                clientSecret=context['client_secret'],
                amount=amount,
                currency=context['currency'],
            )
                order.isPaid = True
                order.paidAt = datetime.now()
                order.save()

                return Response(context, status=status.HTTP_200_OK)
            except stripe.error.StripeError as e:
                return Response({'error_message': str(e)})
        else:
            return Response({'No Order Found'})

    else:
        return Response({'Payment already completed'})

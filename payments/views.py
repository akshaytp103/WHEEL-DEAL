from importlib.resources import Package
import json
import razorpay
from rest_framework.decorators import api_view
from rest_framework.response import Response

from Bookings.serializers import BookingSerializer
from .models import *
from django.conf import settings
from rest_framework import generics
from django.shortcuts import render

@api_view(['POST'])
def start_payment(request):
    # request.data is coming from frontend
    amount = request.data['amount']
    name = request.data['name']
    address = request.data['address'] 
    # slot = request.data['slot']

    # setup razorpay client this is the client to whome user is paying money that's you
    client = razorpay.Client(auth=(settings.RAZORPAY_PUBLIC_KEY,settings.RAZORPAY__SECRET_KEY))
    # create razorpay orderpees.
    payment = client.order.create({"amount": int(amount) * 100, 
                                   "currency": "INR", 
                                   "payment_capture": "1"})

    # we are saving an order with isPaid=False because we've just initialized the order
    # we haven't received the money we will handle the payment succes in next 
    # function
    order = Order.objects.create(order_package_id=name, 
                                 order_amount=amount, 
                                 order_payment_id=payment['id'],
                                #  slot=slot,
                                 address=address)

    serializer = BookingSerializer(order)

    """order response will be 
    {'id': 17, 
    'order_date': '23 January 2021 03:28 PM', 
    'order_product': '**product name from frontend**', 
    'order_amount': '**product amount from frontend**', 
    'order_payment_id': 'order_G3NhfSWWh5UfjQ', # it will be unique everytime
    'isPaid': False}"""

    data = {
        "payment": payment,
        "order": serializer.data
    }
    return Response(data)
from cmath import pi
import email
from importlib.resources import Package
import json
from django import forms
import razorpay
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from Bookings.serializers import BookingSerializer
from .serilalizers import *
from .models import *
from Bookings.models import *
from django.conf import settings
from rest_framework import generics
from django.shortcuts import render

@api_view(['POST'])
def start_payment(request):
    # request.data is coming from frontend
    print(request.data)
    # order_rent=request.data['car']
    amount = request.data['amount'] 
    id = request.data['id']
    

    # setup razorpay client this is the client to whome user is paying money that's you
    # client = razorpay.Client(auth=(settings.RAZORPAY_PUBLIC_KEY,settings.RAZORPAY__SECRET_KEY))
    client = razorpay.Client(auth=('rzp_test_Wg9g7aSl8rGdmP','JhinxMUOsC3sN0oC8SiCsilE'))


    # create razorpay orderpees.
    payment = client.order.create({"amount": int(amount) * 100, 
                                   "currency": "INR", 
                                   "payment_capture": "1"}) 

    # we are saving an order with isPaid=False because we've just initialized the order
    # we haven't received the money we will handle the payment succes in next 
    # function


    order = Order.objects.create( 
                                 order_amount=amount, 
                                 order_payment_id=payment['id'],
                                #  order_rent=order_rent,
                                 )
                                
    print(order)

    serializer = OrderSerializer(order)

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

@api_view(['POST'])
def payment_success(request):
    # request.data is coming from frontend
    res = request.data['response']
    
    """res will be:
    {
        "razorpay_payment_id":"pay_G3NivgSZLx7I9e", 
        "razorpay_order_id": "order_G3NhfSWWh5UfjQ", 
        "razorpay_signature":"76b2accbefde6cd2392b5fbf098ebcbd4cb4ef8b78d62aa5cce553b2014993c0"
    }

    this will come from frontend which we will use to validate and confirm the payment
    """

    ord_id = ""
    raz_pay_id = ""
    raz_signature = ""

    # res.keys() will give us list of keys in res

    for key in res.keys():
        if key == 'razorpay_order_id':
            ord_id = res[key]
        elif key == 'razorpay_payment_id':
            raz_pay_id = res[key]
        elif key == 'razorpay_signature':
            raz_signature = res[key]

    # get order by payment_id which we've created earlier with isPaid=False
    order = Order.objects.get(order_payment_id=ord_id)

    # we will pass this whole data in razorpay client to verify the payment
    data = {
        'razorpay_order_id': ord_id,
        'razorpay_payment_id': raz_pay_id,
        'razorpay_signature': raz_signature
    }
    print(data)

    # client =razorpay.Client(auth=(settings.RAZORPAY_PUBLIC_KEY,settings.RAZORPAY__SECRET_KEY))
    client = razorpay.Client(auth=('rzp_test_Wg9g7aSl8rGdmP','JhinxMUOsC3sN0oC8SiCsilE'))

    # checking if the transaction is valid or not by passing above data dictionary in 
    # razorpay client if it is "valid" then check will return None
    check = client.utility.verify_payment_signature(data)

    if check is  None:
        print("Redirect to error url or error page")
        return Response({'error': 'Something went wrong'})

    # if payment is successful that means check is None then we will turn isPaid=True
    id=request.data['id']
    # slot = request.data['slot']
    package = Order.object.get(id=id)
    package.stock-=1
    package.save()
    booking = Booking.objects.get(id=Booking)
    booking.isbooked=True
    order.isPaid = True
    order.order_status='Approved'
    order.save()

    res_data = {
        'message': 'payment successfully received!'
    }

    return Response(res_data)



def temp_payment(request):
    payment =0
    order=0
    if request.method == 'POST':
        amount = request.POST.get('amount')
        name = request.POST['name']
        # request.session['key'] = name
        print(name)
        

        # client =razorpay.Client(auth=(settings.RAZORPAY_PUBLIC_KEY,settings.RAZORPAY__SECRET_KEY))
        client = razorpay.Client(auth=('rzp_test_Wg9g7aSl8rGdmP','JhinxMUOsC3sN0oC8SiCsilE'))
        payment = client.order.create({"amount": int(amount) * 100, 
                                   "currency": "INR", 
                                   "payment_capture": "1"})
        

        
        
        # user=Account.objects.get(email=request.user.email)
        # booking  = Booking.objects.get(car=name) 
        # print(999999,id,booking)
        user = request.user 
        print(user)
        
        order = Order.objects.create(
                                      
                                      order_amount=amount, 
                                      user_id=request.user.id,
                                      order_payment_id=payment['id'])
        payment['name']=name  
        
    return render(request,'payment.html',{'payment':payment,'order':order})



    # payment status 

def paymentstatus(request):
    status =None
    response = request.POST
    # id = request.data['id']
    # print(id)

    print("ddd",response)

    params_dict = {
        'razorpay_order_id':response['razorpay_order_id'],
        'razorpay_payment_id':response['razorpay_payment_id'],
        'razorpay_signature':response['razorpay_signature']
    }

    client =razorpay.Client(auth=(settings.RAZORPAY_PUBLIC_KEY,settings.RAZORPAY__SECRET_KEY))

   
    status = client.utility.verify_payment_signature(params_dict)
    print(status,'ghg')
    try:
        order = Order.objects.get(order_id=response['razorpay_order_id'])
        order.order_payment_id  = response['razorpay_payment_id']
            
        order.isPaid = True
        order.order_status='Approved'
        order.save()

        name = request.session['key']
        package = Booking.objects.get(id=name)
        print(package)
        package.stock -=1
        package.save()

        print(name,111112)
        #df
        return render(request,'success.html',{'status':True})
    except:
        return render(request,'success.html',{'status':False})
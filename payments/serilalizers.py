from asyncore import write
from dataclasses import field, fields
from email.policy import default
from razorpay import Payment

from wheelproject.Bookings.serializers import BookingSerializer
from .models import *
from rest_framework import serializers



class OrderSerializers(serializers.HyperlinkedModelSerializer):
    url= serializers.HyperlinkedIdentityField(view_name="Payment")
    order=serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault())

    book=BookingSerializer(read_only=True)


    booking_id=serializers.PrimaryKeyRelatedField(
        write_only=True,
        source='booking',
        queryset=Booking.objects.all(),
        label='booking'
    )

    class Meta:
        model=Booking
        fields=['url','choice','user','order_rent','order_amount',
                'order_id','order_payment_id','order_date','order_status','order_total']

        extra_kwargs={
            'order_status':{'read_only':True},
            'order_total':{'read_only':True}
        }
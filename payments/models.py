from tokenize import blank_re
from unittest.util import _MAX_LENGTH
from django.db import models
from Bookings.models import *
from accounts.models import Account


class bookingdetails(models.Model):
    user =models.ForeignKey(Account,on_delete=models.CASCADE)
    car =models.ForeignKey(Car,on_delete=models.CASCADE)
    booking_id=models.AutoField(primary_key=True)




class Order(models.Model):
    choice = ( ('Approved','Approved'),('Cancelled','Cancelled'),('Cancel','Cancel'),('Pending','Pending'))
    # user=models.ForeignKey(Account,on_delete=models.CASCADE,null =True,blank=True)
    # Payment=models.ForeignKey(Payment,on_delete=models.SET_NULL,null=True)
    order_rent = models.ForeignKey(Booking,on_delete=models.CASCADE,null=True,blank=True)
    order_amount = models.CharField(max_length=25)
    user_id=models.CharField(max_length=10,null=True)
    # order_id = models.CharField(max_length=100,blank=True)
    order_payment_id = models.CharField(max_length=100)
    isPaid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now=True,blank=True)
    createdAt = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_status = models.CharField(max_length=50,choices=choice,default='Pending',blank=True)
    order_total = models.IntegerField(null=True,blank=True)
    
    def __str__(self):
        return str(self.order_rent) 
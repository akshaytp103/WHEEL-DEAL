from tokenize import blank_re
from django.db import models
from Bookings.models import *
from accounts.models import Account

# Create your models here.
class Order(models.Model):
    choice = ( ('Approved','Approved'),('Cancelled','Cancelled'),('Cancel','Cancel'),('Pending','Pending'))
    user =models.ForeignKey(Account,on_delete=models.CASCADE,null =True,blank=True)
    order_rent = models.ForeignKey(Booking,on_delete=models.CASCADE,null=True,blank=True)
    order_amount = models.CharField(max_length=25)
    order_id = models.CharField(max_length=100,blank=True)
    order_payment_id = models.CharField(max_length=100)
    isPaid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now=True,blank=True)
    createdAt = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_status = models.CharField(max_length=50,choices=choice,default='Pending',blank=True)
    order_total = models.IntegerField(null=True,blank=True)
    
    def __str__(self):
        return self.order_rent.car
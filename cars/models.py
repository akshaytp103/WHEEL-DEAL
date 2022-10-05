
from accounts.models import *
from django.db import models
from django.contrib.auth.models import User
# from django.utils.text import slugify

# Create your models here.

class Location(models.Model):
    city = models.CharField(max_length=50)
    short_name = models.CharField(max_length=100,null=True)
 
    def __str__(self):
        return self.city

class Dealer(models.Model):
    vendor_name = models.CharField(max_length=100)
    owner = models.ForeignKey(Account, related_name='vendor', on_delete= models.CASCADE, blank=True, null=True)
    GST_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    email = models.EmailField(max_length=150, unique=True, null=True, blank=True)
    mobile = models.CharField(max_length=10, unique=True)
    image = models.ImageField(upload_to='vendors', blank=True, null= True)

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name

    def has_perm(self,perm,obj=None):
        return self.is_active
    
    class Meta:
        ordering = ['-updated_at','-created_at'] 
        
        
        
    
class Car(models.Model):
    name = models.CharField(max_length=150, blank=False, null = False)
    slug = models.SlugField(max_length=100,unique=True,null=True)   
    short_name = models.CharField(max_length=100,null=True)
    code_registration = models.CharField(max_length=20,blank=True,null=True)
    main_location = models.ForeignKey(
        Location, related_name="tracks", on_delete=models.SET_NULL, null=True
    )
    brand = models.CharField(max_length=150, blank=False, null=False)
    model = models.CharField(max_length=150, blank=False, null= False)
    price = models.IntegerField(null=False,blank=False)
    capacity=models.IntegerField(null=False,blank=False)
    owner = models.ForeignKey(Dealer, related_name='posts', on_delete= models.CASCADE, blank=True, null=True)
    creator = models.CharField(max_length=255)
    image = models.ImageField(upload_to='photos',null=True,blank=True)
    speed = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField()  
    date_of_entry = models.DateTimeField(auto_now_add=True)
    on_the_way = models.BooleanField(default=False)
    Flocation = models.CharField(max_length=255, null=True, blank=True)
    to_the_location = models.CharField(max_length=255, null=True, blank=True)
    come_back = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        ordering = ['-updated_at','-created_at'] 

    def __str__(self):
        return self.name
    
    
class Cars_ARC(models.Model):
    id_car = models.CharField(max_length=5)
    id_location = models.CharField(max_length=5)
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=100)
    code_registration = models.CharField(max_length=20)
    creator_ARC = models.CharField(max_length=255)
    change_date = models.DateTimeField(auto_now_add=True)
    on_the_way = models.BooleanField(default=False)
    location = models.CharField(max_length=255, null=True, blank=True)
    to_the_location = models.CharField(max_length=255, null=True, blank=True)
    come_back = models.BooleanField(default=False)
    
    
class Cars_Reservation(models.Model):
    id_cars = models.ForeignKey(
        Car, related_name="carReservations", on_delete=models.SET_NULL, null=True
    )
    client = models.ForeignKey(Account,on_delete=models.CASCADE,blank=True,null=True)
    client_name = models.CharField(max_length=255)
    client_document_type = models.CharField(max_length=50, null=True, blank=True)
    client_document_identification = models.CharField(
        max_length=50, null=True, blank=True
    )
    client_phone = models.CharField(max_length=20, null=True, blank=True)
    client_email = models.EmailField(null=True, blank=True)
    date_from = models.DateTimeField(null=True, blank=True)
    date_to = models.DateTimeField(null=True, blank=True)
    note = models.CharField(max_length=1024, null=True, blank=True)
    date_of_entry = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    location = models.ForeignKey(
        Location,
        related_name="locationReservations",
        on_delete=models.SET_NULL,
        null=True,
    )
    creator = models.CharField(max_length=255)
    owner = models.ForeignKey(Dealer, on_delete= models.CASCADE, blank=True, null=True)
    date_of_change = models.DateTimeField(blank=True, null=True)
    creator_change = models.CharField(max_length=64, blank=True, null=True)
    type_change = models.CharField(max_length=64, blank=True, null=True)
    id_arc = models.CharField(max_length=64, blank=True, null=True)
    
    def __str__(self):
        return self.client_name
    
    
class Cars_Rents(models.Model):
    id_cars = models.ForeignKey(
        Car, related_name="carRents", on_delete=models.SET_NULL, null=True, blank=True
    )
    client = models.ForeignKey(Account,on_delete=models.CASCADE,blank=True,null=True)
    client_name = models.CharField(max_length=255)
    client_document_type = models.CharField(max_length=50, null=True, blank=True)
    client_document_identification = models.CharField(
        max_length=50, null=True, blank=True
    )
    client_phone = models.CharField(max_length=20, null=True, blank=True)
    slug =models.SlugField(null=True)
    date_from = models.DateTimeField(auto_now_add=True)
    date_to = models.DateTimeField(null=True, blank=True)
    total_price = models.CharField(max_length=255,null=True, blank=True)
    total_price_is_paid = models.BooleanField(default=False,null=True, blank=True)
    creator = models.CharField(max_length=255,null=True, blank=True)
    is_active = models.BooleanField(default=True)
    location = models.ForeignKey(
        Location, related_name="locationRents", on_delete=models.SET_NULL, null=True, blank=True
    )
    
    
    def __str__(self):
        return self.client_name

from cars.models import Car
from django.contrib.auth.models import User
from django.db import models


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE,null=True)
    booking_start = models.DateField(null=True)
    booking_end = models.DateField(null=True)
    booking_duration = models.DecimalField(max_digits=3, decimal_places=0,null=True)
    created = models.DateTimeField(auto_now_add=True,null=True) 
    updated = models.DateTimeField(auto_now=True,null=True) 
    total_price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    day_price = models.DecimalField(max_digits=6,default=False, decimal_places=2,null=True  )

    def __str__(self):
        return str(self.car)
    
    class Meta:
        ordering = ['-created']
            
    def save(self, *args, **kwargs):
        self.booking_duration = (self.booking_end - self.booking_start).days
        self.total_price = self.booking_duration * self.day_price
        super(Booking, self).save(*args, **kwargs)
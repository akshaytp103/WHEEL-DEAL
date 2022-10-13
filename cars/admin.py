
from django.contrib import admin
from .models import *

# Register your models here.

class CarModel(admin.ModelAdmin):
        list_display = (
            # "id",
            "name",
            "slug",
            "is_active",
        )
        prepopulated_fields = {"slug": ("name",)}
admin.site.register(Location)
admin.site.register(Dealer)
admin.site.register(Car)
# admin.site.register(Cars_ARC)
# admin.site.register(Cars_Rents)
admin.site.register(Cars_Reservation)

# prepopulated_fields = {'slug': ('name',)}
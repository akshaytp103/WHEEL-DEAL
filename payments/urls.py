from django.urls import path
from . import views

urlpatterns = [
    path('pay/', views.start_payment, name="payment"),
    path('pay/success/', views.payment_success, name="payment_success"),
    path('pays/', views.temp_payment, name="pay"),
    path('status/', views.paymentstatus, name="status")
]
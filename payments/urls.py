from django.urls import path
from . import views

urlpatterns = [
    path('startpayment/', views.start_payment),
    # path('verifySignature/', views.verifySignature),
]
from django.urls import path
from . import views

urlpatterns = [
    path('process/', views.payment_form, name='payment-form'),
    path('<int:payment_id>/', views.payment_detail, name='payment-detail'),
]
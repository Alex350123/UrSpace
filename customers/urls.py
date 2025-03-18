from django.urls import path
from .views import CustomerRegisterView, CustomerLoginView, CustomerRegister, CustomerLogin

urlpatterns = [
    path('api/register/', CustomerRegisterView.as_view(), name='customer-register'),
    path('api/login/', CustomerLoginView.as_view(), name='customer-login'),
    path('register/', CustomerRegister, name='customer-register'),
    path('', CustomerLogin, name='customer-login'),
]
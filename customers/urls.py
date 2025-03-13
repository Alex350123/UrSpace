from django.urls import path
from .views import CustomerRegisterView, CustomerLoginView

urlpatterns = [
    path('api/register/', CustomerRegisterView.as_view(), name='customer-register'),
    path('api/login/', CustomerLoginView.as_view(), name='customer-login'),
]
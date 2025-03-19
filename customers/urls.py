from django.urls import path
from .views import CustomerRegisterView, CustomerLoginView, CustomerRegister, CustomerLogin, CustomerProfile, get_personal_info,\
    OrderPage, load_orders
urlpatterns = [
    path('api/register/', CustomerRegisterView.as_view(), name='customer-register'),
    path('api/login/', CustomerLoginView.as_view(), name='customer-login'),
    path('register/', CustomerRegister, name='customer-register'),
    path('profile/', CustomerProfile, name='customer-profile'),
    path('api/getprofile/', get_personal_info, name='get-personal-info'),
    path('order/', OrderPage, name='order-page'),
    path('api/load_orders/', load_orders, name='load-orders'),
    path('', CustomerLogin, name='customer-login'),
]
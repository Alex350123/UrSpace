from django.urls import path
from .views import OperatorRegisterView, OperatorLoginView, OperatorLogin

urlpatterns = [
    path('api/register/', OperatorRegisterView.as_view(), name='operator-register'),
    path('api/login/', OperatorLoginView.as_view(), name='operator-login-api'),
    path('login/', OperatorLogin, name='operator-login'),
]
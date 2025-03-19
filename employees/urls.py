from django.urls import path
from .views import OperatorRegisterView, OperatorLoginView, OperatorLogin, OperatorHomePage, track_rooms,\
    track_defective, change_availability, change_occupied, repair_defective

urlpatterns = [
    path('api/register/', OperatorRegisterView.as_view(), name='operator-register'),
    path('api/login/', OperatorLoginView.as_view(), name='operator-login-api'),
    path('login/', OperatorLogin, name='operator-login'),
    path('home/', OperatorHomePage, name='operator-home'),
    path('api/trackrooms/', track_rooms, name='track-rooms'),
    path('api/trackdefective/', track_defective, name='track-defective'),
    path('api/change_availability/', change_availability, name='change-availability'),
    path('api/change_occupied/', change_occupied, name='change-occupied'),
    path('api/repair_defective/', repair_defective, name='repair-defective'),
]
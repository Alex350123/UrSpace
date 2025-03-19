from django.urls import path
from .views import CustomerHome, SmallStudyRoomPage, MediumMeetingRoomPage, CoWorkingSpacePage, QuietStudyRoomPage, \
    TemporaryWorkstationPage, get_locations, save_rentals, PaymentPage,rental_summary, payment

urlpatterns = [
    path('home/', CustomerHome, name='home'),
    path('SSR/', SmallStudyRoomPage, name='SmallStudyRoom'),
    path('MMR/', MediumMeetingRoomPage, name='MediumMeetingRoom'),
    path('CWS/', CoWorkingSpacePage, name='CoWorkingSpace'),
    path('QSR/', QuietStudyRoomPage, name='QuietStudyRoom'),
    path('TEMP/', TemporaryWorkstationPage, name='TemporaryWorkstation'),
    path('payment/', PaymentPage, name='Payment'),
    path('api/get_locations/', get_locations, name='get_locations'),
    path('api/save_rentals/', save_rentals, name='save_rentals'),
    path('api/rental_summary/', rental_summary, name='rental_summary'),
    path('api/payment/', payment, name='payment'),

]
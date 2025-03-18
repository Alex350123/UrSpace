from django.contrib import admin
from .models import Location, Room, Rental
# Register your models here.
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('Locationid', 'locationname', 'locationaddress','longitude', 'latitude')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('Roomid','Locationid','roomtype',
    'availability',
    'price',
    'is_defective_light',
    'is_defective_chair',
    'is_defective_socket',
    'is_defective_wifi')

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = (    'Rentalid', 'Customerid',
    'Roomid',
    'rent_date' ,
    'rent_start_time' ,
    'rent_end_time',
    'charge' ,
    'paymentstatus' ,)
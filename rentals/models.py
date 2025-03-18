from django.db import models
import datetime

from customers.models import Customer
# Create your models here.
class Location(models.Model):
    Locationid = models.AutoField(primary_key=True)
    locationname = models.CharField(max_length=50)
    locationaddress = models.CharField(max_length=50)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=False)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=False)
    def __str__(self):
        return self.locationname

class Room(models.Model):
    Roomid = models.AutoField(primary_key=True)
    Locationid = models.ForeignKey(Location, on_delete=models.CASCADE)
    roomtype = models.CharField(blank=False, max_length=50)
    availability = models.BooleanField(default=True)
    price = models.FloatField(default=0)
    is_defective_light = models.BooleanField(default=False)
    is_defective_chair = models.BooleanField(default=False)
    is_defective_socket = models.BooleanField(default=False)
    is_defective_wifi = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.roomname}+ {self.roomtype}"

class Rental(models.Model):
    Rentalid = models.AutoField(primary_key=True)
    Customerid = models.ForeignKey(Customer, on_delete=models.CASCADE)
    Roomid = models.ForeignKey(Room, on_delete=models.CASCADE)
    rent_date = models.DateField(default=datetime.date.today)
    rent_start_time = models.DateTimeField()
    rent_end_time = models.DateTimeField()
    charge = models.FloatField(default=0)
    paymentstatus = models.BooleanField(default=False)

    def __str__(self):
        return f"rent order {self.Rentalid} from {self.rent_start_time} to {self.rent_end_time} at {self.Roomid}"

class Review(models.Model):
    Reviewid = models.AutoField(primary_key=True)
    Customerid = models.ForeignKey(Customer, on_delete=models.CASCADE)
    Roomid = models.ForeignKey(Room, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.Customerid} {self.Roomid}{self.rating}"

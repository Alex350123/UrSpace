from django.test import TestCase
from django.utils import timezone
from .models import Location, Room, Rental
from customers.models import Customer
import datetime

class LocationModelTest(TestCase):
    def test_create_location(self):
        # 测试 Location 模型的创建和字符串表示
        location = Location.objects.create(
            locationname="Central Library",
            locationaddress="123 Main St",
            longitude=-122.4194,
            latitude=37.7749
        )
        self.assertEqual(str(location), "Central Library")

class RoomModelTest(TestCase):
    def setUp(self):
        # 创建一个测试位置
        self.location = Location.objects.create(
            locationname="Central Library",
            locationaddress="123 Main St",
            longitude=-122.4194,
            latitude=37.7749
        )

    def test_create_room(self):
        # 测试 Room 模型的创建和字符串表示
        room = Room.objects.create(
            Locationid=self.location,
            roomtype="Study Room",
            availability=True,
            price=25.0
        )
        self.assertEqual(str(room), f"{room.Roomid}+ Study Room")

class RentalModelTest(TestCase):
    def setUp(self):
        # 创建测试客户和房间
        self.customer = Customer.objects.create(
            firstname="John",
            lastname="Doe",
            email="johndoe@example.com",
            phone="1234567890",
            DOB=datetime.date(1990, 1, 1),
            password="password"
        )
        self.location = Location.objects.create(
            locationname="Central Library",
            locationaddress="123 Main St",
            longitude=-122.4194,
            latitude=37.7749
        )
        self.room = Room.objects.create(
            Locationid=self.location,
            roomtype="Study Room",
            availability=True,
            price=25.0
        )

    def test_create_rental(self):
        # 测试 Rental 模型的创建和字符串表示
        rental = Rental.objects.create(
            Customerid=self.customer,
            Roomid=self.room,
            rent_start_time=timezone.now(),
            rent_end_time=timezone.now() + datetime.timedelta(hours=2),
        )
        self.assertIn("rent order", str(rental))

class ReviewModelTest(TestCase):
    def setUp(self):
        # 创建测试位置
        self.location = Location.objects.create(
            locationname="Meeting Center",
            locationaddress="456 Side St",
            longitude=-122.4233,
            latitude=37.7777
        )
        # 创建测试客户和房间
        self.customer = Customer.objects.create(
            firstname="Alice",
            lastname="Wonder",
            email="alice@example.com",
            phone="0987654321",
            DOB=datetime.date(1992, 2, 2),
            password="securepassword"
        )
        self.room = Room.objects.create(
            Locationid=self.location,
            roomtype="Meeting Room",
            availability=True,
            price=30.0
        )

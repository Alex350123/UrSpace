import base64
import binascii
import os
from django.shortcuts import render
from django.utils.timezone import localtime
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterCustomerSerializer
from .models import Customer, CustomerToken
from .utils import CustomerTokenAuthentication
from cryptography.fernet import Fernet
from django.conf import settings
from rentals.models import Rental

cipher = Fernet(settings.FERNET_KEY.encode())
# Create your views here.
class CustomerRegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        serializer = RegisterCustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Customer registered successfully"}, status=status.HTTP_201_CREATED)
        else:
            print("Register Failed", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Customer.objects.get(email=email)
            print(f"User found: {user.email}")

            if user.check_password(password):
                print("Password matches")
                CustomerToken.objects.filter(customer=user).delete()
                token = CustomerToken(customer=user)
                token.key = binascii.hexlify(os.urandom(20)).decode()
                token.save()

                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                print("Password does not match")
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        except Customer.DoesNotExist:
            print("User does not exist")
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


def is_encrypted(value):

    try:

        base64.b64decode(value.encode())
        return True
    except Exception:
        return False

@api_view(['GET'])
@authentication_classes([CustomerTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_personal_info(request):
    customer = request.user

    if not customer:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    try:

        decrypted_firstname = cipher.decrypt(customer.firstname.encode()).decode('utf-8')
        decrypted_lastname = cipher.decrypt(customer.lastname.encode()).decode('utf-8')
        decrypted_phone = cipher.decrypt(customer.phone.encode()).decode('utf-8')

    except Exception as e:
        return Response({"error": "Decryption failed", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({
        "firstName": decrypted_firstname,
        "secondName": decrypted_lastname,
        "dateOfBirth": customer.DOB.strftime('%Y-%m-%d') if customer.DOB else None,
        "phoneNumber": decrypted_phone,
        "email": customer.email
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([CustomerTokenAuthentication])
@permission_classes([IsAuthenticated])
def load_orders(request):
    customer = request.user
    rentals = Rental.objects.filter(Customerid=customer).order_by('-rent_date', '-rent_start_time')

    order_list = []
    for rental in rentals:
        room = rental.Roomid
        location = room.Locationid
        order_list.append({
            "customerName": f"{customer.get_decrypted_firstname()} {customer.get_decrypted_lastname()}",
            "roomType": room.roomtype,
            "location": location.locationaddress,
            "date": rental.rent_date.strftime("%Y-%m-%d"),
            "timeSlot": f"{localtime(rental.rent_start_time).strftime('%H:%M')} - {localtime(rental.rent_end_time).strftime('%H:%M')}",
            "totalPrice": f"${rental.charge:.2f}"
        })

    return Response(order_list, status=status.HTTP_200_OK)

def CustomerRegister(request):
    return render(request,'Customer_Register.html')

def CustomerLogin(request):
    return render(request,'Customer_Login.html')

def CustomerProfile(request):
    return render(request, 'Personal_Home.html')

def OrderPage(request):
    return render(request, 'Order.html')
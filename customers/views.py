import binascii
import os
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterCustomerSerializer
from .models import Customer, CustomerToken
# Create your views here.
class CustomerRegisterView(APIView):
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
            # find the user
            user = Customer.objects.get(email=email)
            print(f"User found: {user.email}")

            # check if password matches
            if user.check_password(password):
                print("Password matches")
                token, created = CustomerToken.objects.get_or_create(customer=user)
                if created:
                    token.key = binascii.hexlify(os.urandom(20)).decode()
                    token.save()
                return Response({'token': token.key}, status=status.HTTP_200_OK)

            else:
                print("Password does not match")
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        except Customer.DoesNotExist:
            print("User does not exist")
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
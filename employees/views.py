import binascii
import os

from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import OperatorRegisterSerializer
from .models import Operator, OperatorToken
# Create your views here.
class OperatorRegisterView(APIView):
    def post(self, request, format=None):
        serializer = OperatorRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Operator registered successfully"}, status=status.HTTP_201_CREATED)
        else:
            print("Register Failed", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OperatorLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Operator.objects.get(email=email)
            print(f"User found: {user.email}")

            if user.check_password(password):
                print("Password matches")
                # 正确的方法是直接操作 OperatorToken 模型
                OperatorToken.objects.filter(operator=user).delete()

                token = OperatorToken(operator=user)
                token.key = binascii.hexlify(os.urandom(20)).decode()
                token.save()

                return Response({"token": token.key}, status=status.HTTP_200_OK)

            else:
                print("Password does not match")
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        except Operator.DoesNotExist:
            print("User does not exist")
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


def OperatorLogin(request):
    return render(request,'Operator_Login.html')
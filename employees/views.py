import binascii
import os
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import OperatorRegisterSerializer
from .models import Operator, OperatorToken
from .utils import OperatorTokenAuthentication
from rentals.models import Room
from django.db.models import Q
# Create your views here.
class OperatorRegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        serializer = OperatorRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Operator registered successfully"}, status=status.HTTP_201_CREATED)
        else:
            print("Register Failed", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OperatorLoginView(APIView):
    permission_classes = [AllowAny]
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


@api_view(['GET'])
@authentication_classes([OperatorTokenAuthentication])
@permission_classes([IsAuthenticated])
def track_rooms(request):
    rooms = Room.objects.all().values('Roomid', 'roomtype', 'availability')
    return Response(list(rooms), status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([OperatorTokenAuthentication])
@permission_classes([IsAuthenticated])
def track_defective(request):
    defective_rooms = Room.objects.filter(
        Q(is_defective_light=True) |
        Q(is_defective_chair=True) |
        Q(is_defective_socket=True) |
        Q(is_defective_wifi=True)
    ).values('Roomid', 'roomtype', 'availability', 'is_defective_light', 'is_defective_chair', 'is_defective_socket',
             'is_defective_wifi')

    return Response(list(defective_rooms), status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([OperatorTokenAuthentication])
@permission_classes([IsAuthenticated])
def change_availability(request):
    room_id = request.data.get("room_id")

    if not room_id:
        return Response({"error": "Room ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    room = get_object_or_404(Room, Roomid=room_id)
    room.availability = False
    room.save()

    return Response({"message": f"Room {room_id} availability updated"}, status=status.HTTP_200_OK)

def OperatorHomePage(request):
    return render(request,'Operator_Home.html')


def OperatorLogin(request):
    return render(request,'Operator_Login.html')


@api_view(['POST'])
@authentication_classes([OperatorTokenAuthentication])
@permission_classes([IsAuthenticated])
def change_occupied(request):
    room_id = request.data.get("room_id")

    if not room_id:
        return Response({"error": "Room ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        room = Room.objects.get(Roomid=room_id)
        room.availability = not room.availability
        room.save()
        return Response({"message": f"Room {room_id} availability changed to {'Available' if room.availability else 'Unavailable'}"},
                        status=status.HTTP_200_OK)

    except Room.DoesNotExist:
        return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes([OperatorTokenAuthentication])
@permission_classes([IsAuthenticated])
def repair_defective(request):
    room_id = request.data.get("room_id")

    if not room_id:
        return Response({"error": "Room ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        room = Room.objects.get(Roomid=room_id)


        room.is_defective_light = False
        room.is_defective_chair = False
        room.is_defective_socket = False
        room.is_defective_wifi = False
        room.save()

        return Response({"message": f"Room {room_id} defects repaired successfully"}, status=status.HTTP_200_OK)

    except Room.DoesNotExist:
        return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

import re
from time import localtime

from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes# Create your views here.
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Location, Room, Rental

from customers.models import Customer, CustomerToken
from customers.utils import CustomerTokenAuthentication
def CustomerHome(request):
    return render(request,'Customer_Home.html')

def SmallStudyRoomPage(request):
    return render(request,'Type1_Details.html')

def MediumMeetingRoomPage(request):
    return render(request,'Type2_Details.html')

def CoWorkingSpacePage(request):
    return render(request,'Type3_Details.html')

def QuietStudyRoomPage(request):
    return render(request,'Type4_Details.html')

def TemporaryWorkstationPage(request):
    return render(request,'Type5_Details.html')

def PaymentPage(request):
    return render(request,'Rent_Payment.html')

@api_view(['GET'])
@authentication_classes([CustomerTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_locations(request):
    print("get_locations debug, request.user: ", request.user)
    roomtype = request.GET.get('roomtype')
    print("get_locations debug, Authorization Header:", request.headers.get('Authorization'))

    if roomtype:
        rooms = Room.objects.filter(roomtype=roomtype, availability=True).select_related('Locationid')
        locations = [
            {
                'room_id': room.Roomid,  # 添加 room_id
                'location_id': room.Locationid.Locationid,
                'locationname': room.Locationid.locationname
            }
            for room in rooms
        ]
    else:
        print("No room type returned")
        locations = [
            {
                'location_id': loc.Locationid,
                'locationname': loc.locationname,
                'room_id': None
            }
            for loc in Location.objects.all()
        ]

    return JsonResponse(list(locations), safe=False)



from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Rental, Room

@api_view(['POST'])
@authentication_classes([CustomerTokenAuthentication])
@permission_classes([IsAuthenticated])
def save_rentals(request):
    """
    API 用于保存用户的租赁订单
    """
    customer = request.user  # 通过 token 获取当前登录用户
    data = request.data

    # 获取前端提交的数据
    room_id = data.get('room_id')
    rent_date = data.get('rent_date')  # YYYY-MM-DD 格式
    rent_start_time = data.get('rent_start_time')  # HH:mm 格式
    rent_end_time = data.get('rent_end_time')  # HH:mm 格式

    # 确保所有必需字段都已提供
    if not all([room_id, rent_date, rent_start_time, rent_end_time]):
        return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

    # 查找房间
    room = get_object_or_404(Room, Roomid=room_id)

    # 确保房间可用
    if not room.availability:
        return Response({'error': 'Selected room is not available'}, status=status.HTTP_400_BAD_REQUEST)

    # 解析日期和时间，并确保有时区信息
    try:
        rent_start_datetime = timezone.make_aware(parse_datetime(f"{rent_date}T{rent_start_time}:00"))
        rent_end_datetime = timezone.make_aware(parse_datetime(f"{rent_date}T{rent_end_time}:00"))

        # 确保结束时间晚于开始时间
        if rent_end_datetime <= rent_start_datetime:
            return Response({'error': 'End time must be later than start time'}, status=status.HTTP_400_BAD_REQUEST)

        # 计算租赁费用
        duration_hours = (rent_end_datetime - rent_start_datetime).total_seconds() / 3600
        total_charge = duration_hours * room.price  # 价格 = 小时数 * 房间单价
    except Exception as e:
        return Response({'error': f'Invalid date or time format: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    # 创建租赁订单
    rental = Rental.objects.create(
        Customerid=customer,
        Roomid=room,
        rent_date=rent_start_datetime.date(),
        rent_start_time=rent_start_datetime,
        rent_end_time=rent_end_datetime,
        charge=total_charge,
        paymentstatus=False,  # 默认未支付
        created_at=timezone.now()  # 记录创建时间
    )

    return Response({
        'message': 'Rental saved successfully',
        'rental_id': rental.Rentalid,
        'total_charge': total_charge,
        'payment_status': bool(rental.paymentstatus)  # ✅ 转换为布尔值，防止 JSON 解析错误
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@authentication_classes([CustomerTokenAuthentication])
@permission_classes([IsAuthenticated])
def rental_summary(request):
    rental_id = request.GET.get('rental_id')
    if not rental_id:
        return Response({"error": "Rental ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    rental = get_object_or_404(Rental, Rentalid=rental_id)
    room = rental.Roomid
    location = room.Locationid

    created_at = rental.created_at
    if created_at:
        created_at = timezone.localtime(created_at).strftime("%Y-%m-%d %H:%M:%S")

    return Response({
        "rental_id": rental.Rentalid,
        "location_name": location.locationname,
        "location_address": location.locationaddress,
        "longitude": float(location.longitude),
        "latitude": float(location.latitude),
        "created_at": created_at,
        "total_price": f"${rental.charge:.2f}"
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([CustomerTokenAuthentication])
@permission_classes([IsAuthenticated])
def payment(request):
    Rental_id = request.data.get('ride_id')
    bankcard = request.data.get('bankcard')
    cvv = request.data.get('cvv')

    if not all([Rental_id, bankcard, cvv]):
        return Response({"detail": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        rental = Rental.objects.get(Rentalid=Rental_id, Customerid=request.user)
        if rental.paymentstatus:
            return Response({"detail": "Rental has already been paid."}, status=status.HTTP_400_BAD_REQUEST)

        rental.paymentstatus = True
        rental.save()
        return Response({"message": "Payment successful", "total_charge": f"${rental.charge:.2f}"}, status=status.HTTP_200_OK)

    except Rental.DoesNotExist:
        return Response({"detail": "Rental not found."}, status=status.HTTP_404_NOT_FOUND)

def validate_card_number(card_number):
    return re.fullmatch(r"\d{13,19}", card_number) is not None

def validate_cvv(cvv):
    return re.fullmatch(r"\d{3,4}", cvv) is not None
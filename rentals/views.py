from django.http import JsonResponse
from django.shortcuts import render
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
                'room_id': None  # 如果没有房间信息
            }
            for loc in Location.objects.all()
        ]

    return JsonResponse(list(locations), safe=False)



@api_view(['POST'])
@authentication_classes([CustomerTokenAuthentication])
@permission_classes([IsAuthenticated])
def save_rentals(request):
    """
    API 用于保存用户的租赁订单
    """
    customer = request.user  # 通过 token 获取当前登录用户
    data = request.data

    print("DEBUG: Received request to save_rentals")
    print("DEBUG: Request user =", customer)
    print("DEBUG: Request data =", data)

    # 获取前端提交的数据
    room_id = data.get('room_id')
    rent_date = data.get('rent_date')
    rent_start_time = data.get('rent_start_time')
    rent_end_time = data.get('rent_end_time')

    # 确保所有必需字段都已提供
    if not all([room_id, rent_date, rent_start_time, rent_end_time]):
        return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

    # 查找房间
    room = get_object_or_404(Room, Roomid=room_id)

    # 确保房间可用
    if not room.availability:
        return Response({'error': 'Selected room is not available'}, status=status.HTTP_400_BAD_REQUEST)

    # 解析日期和时间
    try:
        print(f"DEBUG: Parsing datetime {rent_date}T{rent_start_time}:00 and {rent_date}T{rent_end_time}:00")
        rent_start_datetime = parse_datetime(f"{rent_date}T{rent_start_time}:00")
        rent_end_datetime = parse_datetime(f"{rent_date}T{rent_end_time}:00")

        if rent_start_datetime is None or rent_end_datetime is None:
            return Response({'error': 'Invalid datetime format'}, status=status.HTTP_400_BAD_REQUEST)

        # 确保结束时间晚于开始时间
        if rent_end_datetime <= rent_start_datetime:
            return Response({'error': 'End time must be later than start time'}, status=status.HTTP_400_BAD_REQUEST)

        # 计算租赁费用
        duration_hours = (rent_end_datetime - rent_start_datetime).total_seconds() / 3600
        total_charge = duration_hours * room.price
    except Exception as e:
        return Response({'error': f'Error parsing date/time: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    # 创建租赁订单
    rental = Rental.objects.create(
        Customerid=customer,
        Roomid=room,
        rent_date=rent_start_datetime.date(),
        rent_start_time=rent_start_datetime,
        rent_end_time=rent_end_datetime,
        charge=total_charge,
        paymentstatus=False
    )

    return Response({
        'message': 'Rental saved successfully',
        'rental_id': rental.Rentalid,
        'total_charge': total_charge,
        'payment_status': rental.paymentstatus
    }, status=status.HTTP_201_CREATED)

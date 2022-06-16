from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from .models import Attendance, User
from .serializers import RegisterSerializer, AttendanceSerializer

from HrSystemApi.decorators import unauthenticated_user, admin_only
from .helpers import user_info

# Create your views here.

@api_view(['POST'])
@unauthenticated_user
def login(request):    
    serializer = AuthTokenSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.validated_data['user']
        _, token = AuthToken.objects.create(user)
        return Response({
            'user_data': user_info(user),
            'token': token
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['POST'])
@unauthenticated_user
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        return Response({
            "user_info": user_info(user),
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def get_user(request):
    user = request.user
    if user.is_authenticated:
    
        user_role = user.groups.all()[0].name

        return Response({
            'user_data': user_info(user),
            'user_role': user_role,
        }, status=status.HTTP_200_OK)

    return Response({'Erorr': 'Not authentication'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['post'])
def check_in(request):
    user = request.user
    
    # Check if user login by Token
    if not user.is_authenticated:
        return Response({"Erorr": 'You are not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

    # Check if employee Check-in before that
    if user.attendance.all().filter(check_out=None):
        return Response({"Error" : "You must Check-Out first Or You can't check-in twice in a row"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = AttendanceSerializer(data=request.data)
    if serializer.is_valid():
        # Check if employee check-in late
        if str(serializer.validated_data['check_in']) > '09:00:00':
            serializer.validated_data['arrive'] = 'Arrival late'
        
        # Recording the employee in the attendance table
        serializer.save(employee=user)

        return Response({
            'PK': serializer.data['id'],
            'Employee': serializer.data['employee'],
            'Check-in': serializer.data['check_in'],
            'Arrive': serializer.data['arrive'],
            'Day': serializer.data['day'],

            }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['post'])
def check_out(request, attendance_pk):
    attendance = get_object_or_404(Attendance, pk=attendance_pk)
    user = request.user
    # Check if user login by Token
    if not user.is_authenticated:
        return Response({"Erorr": 'You are not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

    # Check if this attendance for the correct employee
    if attendance.employee != user:
        return Response({"Error": f"You Can't Check-out to another empolyee."}, status=status.HTTP_400_BAD_REQUEST)

    # Empolyee can't check-out with out check-in || check-out twice in a row
    if attendance.check_out != None:
        return Response({"Error": "You are already Check-out. Or You can't check-out twice in a row."}, status=status.HTTP_400_BAD_REQUEST)

    serializer = AttendanceSerializer(instance=attendance, data=request.data)
    if serializer.is_valid():
        
        # Check-out must be always bigger than check-in time.
        if serializer.validated_data['check_out'] < attendance.check_in:
            return Response({"Error": "Check-out must be always bigger than check-in time."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if employee check-out early
        if str(serializer.validated_data['check_out']) < '17:00:00':
            serializer.validated_data['leave'] = 'Left early'        

        serializer.save()
    
        # Use signals to set the value of each work_hours, total_overtime_hours

        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def check_in_again(request, attendance_pk):
    attendance = get_object_or_404(Attendance, pk=attendance_pk)
    user = request.user
    # Check if user login by Token
    if not user.is_authenticated:
        return Response({"Erorr": 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Check if this attendance for the correct employee
    if attendance.employee != user:
        return Response({"Error": "You Can't Check-in to another Empolyee."}, status=status.HTTP_400_BAD_REQUEST)

    serializer = AttendanceSerializer(instance=attendance, data=request.data)
    if serializer.is_valid():
        # Check if check-in is sent
        try:
            serializer.validated_data['check_in']
        except KeyError:
            return Response({"Error": "You must send ['check_in'] in your request."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check-in in this case must be always bigger than check-out time.
        if serializer.validated_data['check_in'] <= attendance.check_out:
            return Response({"Error": "Check-in must be always bigger than check-out time."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Make check-out None as employee now in company
        attendance.check_out = None

        serializer.save()
        return Response({
            'PK': serializer.data['id'],
            'Employee': serializer.data['employee'],
            'Check-in': serializer.data['check_in'],
            'Work-Hours': serializer.data['work_hours'],
            'Arrive': serializer.data['arrive'],
            'Day': serializer.data['day'],

        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def check_out_again(request, attendance_pk):
    attendance = get_object_or_404(Attendance, pk=attendance_pk)
    user = request.user
    # Check if user login by Token
    if not user.is_authenticated:
        return Response({"Erorr": 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)   
    
    # Check if this attendance for the correct employee
    if attendance.employee != user:
        return Response({"Error": "You Can't Check-out to another Empolyee."}, status=status.HTTP_400_BAD_REQUEST)

    # Empolyee can't check-out with out check-in || check-out twice in a row
    if attendance.check_out != None:
        return Response({"Error": "You are already Check-out. Or You can't check-out twice in a row."}, status=status.HTTP_400_BAD_REQUEST)

    serializer = AttendanceSerializer(instance=attendance, data=request.data)
    if serializer.is_valid():
        # Check if check-out is sent
        try:
            serializer.validated_data['check_out']
        except KeyError:
            return Response({"Error": "You must send ['check_out'] in your request."}, status=status.HTTP_400_BAD_REQUEST)

        # Check-out must be always bigger than check-in time.
        if serializer.validated_data['check_out'] <= attendance.check_in:
            return Response({"Error": "Check-out must be always bigger than check-in time."}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        # use signals to assigment work_hours & total_overtime_hours
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# For Employee
@api_view(['GET'])
def list_attendances(request):
    user = request.user
    # Check if user login by Token
    if not user.is_authenticated:
        return Response({"Erorr": 'User not authenticated'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Get all attendance records completed and associated with this employee
    employee_attendances = user.attendance.all().exclude(check_out=None)
    serializer = AttendanceSerializer(employee_attendances, many=True)
    
    # If employee has records
    if serializer:
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response({"detail": "OoPs!...You don't have any attendance records."}, status=status.HTTP_404_NOT_FOUND)

    
# For admin
@api_view(['GET'])
@admin_only
def list_attendances_all(request):
    # Get all attendance records completed
    all_attendances = Attendance.objects.all().exclude(check_out=None)
    serializer = AttendanceSerializer(all_attendances, many=True)
    # If employees has records
    if serializer:    
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response({"detail": "OoPs!...No attendance records yet."}, status=status.HTTP_404_NOT_FOUND)


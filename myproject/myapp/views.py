from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response


class studentUserRegistrationView(APIView):
  def post(self, request, format=None):
    serializer = studentUserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()
    # token = get_tokens_for_user(user)
    return Response({'Done':'Registration Successful'}, status=status.HTTP_201_CREATED)


class teacherUserRegistrationView(APIView):
  def post(self, request, format=None):
    serializer = teacherUserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()
    # token = get_tokens_for_user(user)
    return Response({'Done':'Registration Successful'}, status=status.HTTP_201_CREATED)


class UserstudentLoginView(APIView):
    def post(self, request):
        serializer = studentUserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            attendance = user.attendance
            serialized_data = serializer.data
            serialized_data['attendance'] = attendance
            return Response({'msg': 'Login successful', 'data': serialized_data})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginteacherView(APIView):
    def post(self, request):
        serializer = teacherUserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            if user.is_teacher:
                tokens = get_tokens_for_user(user)
                return Response({'access_token': tokens['access'], 'refresh_token': tokens['refresh']})
            return Response({'msg': 'You are not teacher'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateAttendancePercentageView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        email = request.data.get('email')
        attendance_percentage = request.data.get('attendance_percentage')

        try:
            user = studentUser.objects.get(email=email)
        except studentUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user.attendance = attendance_percentage
        user.save()

        return Response({'msg': 'Attendance percentage updated successfully'})
        
    
    
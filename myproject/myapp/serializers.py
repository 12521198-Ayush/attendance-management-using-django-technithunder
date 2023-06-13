from rest_framework import serializers
from .models import *


class teacherUserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name','is_teacher' ,'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2 :
            raise serializers.ValidationError("Password and Confirm Password do not match")
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError("Password must contain at least one digit")
        if not any(char.isalpha() for char in password):
            raise serializers.ValidationError("Password must contain at least one letter")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user( **validated_data)
        return user



class studentUserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = studentUser
        fields = ['email', 'name','password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2 :
            raise serializers.ValidationError("Password and Confirm Password do not match")
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError("Password must contain at least one digit")
        if not any(char.isalpha() for char in password):
            raise serializers.ValidationError("Password must contain at least one letter")

        return attrs
    
    

    def create(self, validated_data):
        user = studentUser.objects.create_user( **validated_data)
        return user



from rest_framework import serializers

class teacherUserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid email or password")
            if not user.check_password(password):
                raise serializers.ValidationError("Invalid email or password")
        else:
            raise serializers.ValidationError("Both email and password are required")

        attrs['user'] = user
        return attrs


class studentUserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = studentUser
        fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            
            try:
                user = studentUser.objects.get(email=email)
            except studentUser.DoesNotExist:
                raise serializers.ValidationError("Invalid email or password")
            if not user.check_password(password):
                raise serializers.ValidationError("Invalid email or password")
        else:
            raise serializers.ValidationError("Both email and password are required")

        attrs['user'] = user
        return attrs

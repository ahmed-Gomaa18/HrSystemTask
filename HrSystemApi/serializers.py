from django.contrib.auth.models import User
from rest_framework import serializers, validators

from .models import Attendance

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "email", "first_name", "last_name")
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(), f"A user with that Email already exists."
                    )
                ],
            },
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"]
        )
        return user



class AttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = ['id', 'employee', 'total_overtime_hours', 'check_in', 'check_out', 'work_hours', 'arrive', 'leave', 'day']

    # Custom validator fields
    def validate_check_in(self, check_in: str) -> dict:
        if not check_in:
            raise serializers.ValidationError({'erorr' : 'blank'})
        return check_in


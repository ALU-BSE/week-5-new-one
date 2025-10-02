from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from users.models import Passenger, Rider

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
            "phone_number",
            "user_type",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "user_type",
            "date_joined",
        )
        read_only_fields = ("id", "date_joined")


class PassengerSerializer(serializers.ModelSerializer):
    """Serializer for passenger profile"""

    user = UserSerializer(read_only=True)

    class Meta:
        model = Passenger
        fields = (
            "id",
            "user",
            "passenger_id",
            "preferred_payment_method",
            "home_address",
            "profile_picture",
            "preferred_language",
            "emergency_contact",
            "is_verified",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "passenger_id",
            "is_verified",
            "created_at",
            "updated_at",
        )


class RiderSerializer(serializers.ModelSerializer):
    """Serializer for rider profile"""

    user = UserSerializer(read_only=True)

    class Meta:
        model = Rider
        fields = (
            "id",
            "user",
            "profile_picture",
            "license_number",
            "license_picture",
            "id_number_picture",
            "verification_status",
            "verification_notes",
            "is_available",
            "current_latitude",
            "current_longitude",
            "average_rating",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "verification_status",
            "verification_notes",
            "average_rating",
            "created_at",
            "updated_at",
        )

from rest_framework import serializers
from .models import User


class SignupSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=4
    )

    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password",
        ]

    def create(self, validated_data):

        password = validated_data.pop("password")

        user = User(
            username=validated_data["email"],
            **validated_data
        )

        user.set_password(password)

        user.save()

        return user
    
    
    
from django.contrib.auth import authenticate
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()

    password = serializers.CharField()

    def validate(self, attrs):

        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            username=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid credentials"
            )

        attrs["user"] = user

        return attrs
    
    
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "role",
            "phone_number",
        ]
        
class ReceptionistCreateSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User(
            role="receptionist",
            **validated_data
        )

        user.username = user.email
        user.set_password(password)
        user.save()

        return user
    
    
    
    
class StaffCreateSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "salary",
            "password"
        ]

    def create(self, validated_data):

        password = validated_data.pop("password")

        user = User(
        username=validated_data["email"],
        email=validated_data["email"],
        role="staff",
        first_name=validated_data["first_name"],
        last_name=validated_data.get("last_name", ""),
        phone_number=validated_data["phone_number"],
        salary=validated_data["salary"],
    )

        user.set_password(password)
        user.save()

        return user
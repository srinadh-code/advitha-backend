from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import SignupSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer

from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer

class SignupAPIView(APIView):

    def post(self, request):

        serializer = SignupSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                "message": "Account created successfully"
            },
            status=status.HTTP_201_CREATED
        )
        
class LoginAPIView(APIView):

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "email": user.email,
                "role": "admin" if user.is_superuser else user.role,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        })
        
        
class MeAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(
            request.user
        )

        return Response(
            serializer.data
        )
        
from rest_framework.permissions import IsAuthenticated
from.serializers import ReceptionistCreateSerializer
class CreateReceptionistAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role != "admin":
            return Response(
                {"error": "Only admin can view receptionists"},
                status=403
            )

        receptionists = User.objects.filter(
            role="receptionist"
        ).values(
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number"
        )

        return Response(receptionists)

    def post(self, request):

        if request.user.role != "admin":
            return Response(
                {"error": "Only admin can create receptionists"},
                status=403
            )

        serializer = ReceptionistCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {"message": "Receptionist created successfully"},
            status=201
        )

    def delete(self, request, receptionist_id):

        if request.user.role != "admin":
            return Response(
                {"error": "Only admin can delete receptionists"},
                status=403
            )

        try:
            receptionist = User.objects.get(
                id=receptionist_id,
                role="receptionist"
            )
        except User.DoesNotExist:
            return Response(
                {"error": "Receptionist not found"},
                status=404
            )

        receptionist.delete()

        return Response(
            {"message": "Receptionist deleted successfully"}
        )


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User, PasswordResetOTP
from .password_reset_serializers import (
    ForgotPasswordSerializer
)
from .email_utils import (
    generate_otp,
    send_otp_email
)


class ForgotPasswordAPIView(APIView):

    def post(self, request):

        serializer = ForgotPasswordSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(
                email=email
            )

        except User.DoesNotExist:

            return Response(
                {
                    "error": "Email not found"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        PasswordResetOTP.objects.filter(
            user=user
        ).delete()

        otp = generate_otp()
        print("GENERATED OTP =", otp)

        PasswordResetOTP.objects.create(
            user=user,
            otp=otp
        )

        send_otp_email(
            email,
            otp
        )

        return Response(
            {
                "message": "OTP sent successfully"
            },
            status=status.HTTP_200_OK
        )
from .models import User, PasswordResetOTP
from .password_reset_serializers import VerifyOTPSerializer, ResetPasswordSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class VerifyOTPAPIView(APIView):

    def post(self, request):

        serializer = VerifyOTPSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        try:
            user = User.objects.get(
                email=email
            )

        except User.DoesNotExist:

            return Response(
                {
                    "error": "User not found"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        otp_record = PasswordResetOTP.objects.filter(
            user=user,
            otp=otp
        ).first()

        if not otp_record:
            return Response(
                {
                    "error": "Invalid OTP"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "message": "OTP verified successfully"
            },
            status=status.HTTP_200_OK
        )
        
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .models import PasswordResetOTP


class ResetPasswordAPIView(APIView):

    def post(self, request):

        serializer = ResetPasswordSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]
        password = serializer.validated_data["password"]

        try:
            user = User.objects.get(
                email=email
            )

        except User.DoesNotExist:

            return Response(
                {
                    "error": "User not found"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        otp_record = PasswordResetOTP.objects.filter(
            user=user,
            otp=otp
        ).first()

        if not otp_record:

            return Response(
                {
                    "error": "Invalid OTP"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(password)
        user.save()

        otp_record.delete()

        return Response(
            {
                "message":
                "Password reset successfully"
            },
            status=status.HTTP_200_OK
        )
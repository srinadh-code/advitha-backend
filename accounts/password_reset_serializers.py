# from rest_framework import serializers


# class ForgotPasswordSerializer(serializers.Serializer):
#     email = serializers.EmailField()
    
    
    
# # accounts/password_reset_serializers.py

# from rest_framework import serializers


# class VerifyOTPSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     otp = serializers.CharField(max_length=6)
    
    
    
# from rest_framework import serializers


# class ResetPasswordSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     otp = serializers.CharField(max_length=6)
#     password = serializers.CharField(
#         min_length=4
#     )


from rest_framework import serializers


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    password = serializers.CharField(
        min_length=8
    )
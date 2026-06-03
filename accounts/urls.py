from django.urls import path

from .views import SignupAPIView,LoginAPIView,MeAPIView,CreateReceptionistAPIView,ForgotPasswordAPIView,VerifyOTPAPIView,ResetPasswordAPIView

urlpatterns = [

    path("signup/",SignupAPIView.as_view(),name="signup" ),
    path("login/",LoginAPIView.as_view(),),
    path("me/",MeAPIView.as_view(),),
    path("receptionists/create/",CreateReceptionistAPIView.as_view()),     

    path("forgot-password/",ForgotPasswordAPIView.as_view()),
    path("verify-otp/",VerifyOTPAPIView.as_view()),
    path("reset-password/",ResetPasswordAPIView.as_view(),),
]


from django.urls import path

from .views import SignupAPIView,LoginAPIView,MeAPIView,CreateReceptionistAPIView,ForgotPasswordAPIView,VerifyOTPAPIView,ResetPasswordAPIView
from .views import GoogleLoginAPIView,CreateStaffAPIView
urlpatterns = [

    path("signup/",SignupAPIView.as_view(),name="signup" ),
    path("login/",LoginAPIView.as_view(),name="login"),
    path("me/",MeAPIView.as_view(),name="me"),  

    path("forgot-password/",ForgotPasswordAPIView.as_view(),name="forgot-password"),
    path("verify-otp/",VerifyOTPAPIView.as_view(),name="verify-otp"),
    path("reset-password/",ResetPasswordAPIView.as_view(),name="reset-password"),
    
    path("receptionists/create/",CreateReceptionistAPIView.as_view()),   
    path("receptionists/<int:receptionist_id>/",   CreateReceptionistAPIView.as_view()  ),
    path("google-login/",GoogleLoginAPIView.as_view(),),
    path(
    "staff/",
    CreateStaffAPIView.as_view()
),

path(
    "staff/<int:staff_id>/",
    CreateStaffAPIView.as_view()
),
]
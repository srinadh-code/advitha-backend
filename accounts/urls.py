from django.urls import path

from .views import SignupAPIView,LoginAPIView,MeAPIView,CreateReceptionistAPIView,ForgotPasswordAPIView,VerifyOTPAPIView,ResetPasswordAPIView
from .views import GoogleLoginAPIView,CreateStaffAPIView
urlpatterns = [

    path("signup/",SignupAPIView.as_view(),name="signup" ),
    path("login/",LoginAPIView.as_view(),),
    path("me/",MeAPIView.as_view(),),  

    path("forgot-password/",ForgotPasswordAPIView.as_view()),
    path("verify-otp/",VerifyOTPAPIView.as_view()),
    path("reset-password/",ResetPasswordAPIView.as_view(),),
    
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
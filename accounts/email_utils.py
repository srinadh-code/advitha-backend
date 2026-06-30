# import random

# import sib_api_v3_sdk
# from django.conf import settings


# def generate_otp():
#     return str(
#         random.randint(
#             100000,
#             999999
#         )
#     )


# def send_otp_email(email, otp):

#     configuration = sib_api_v3_sdk.Configuration()

#     configuration.api_key["api-key"] = (
#         settings.BREVO_API_KEY
#     )

#     api_instance = (
#         sib_api_v3_sdk.TransactionalEmailsApi(
#             sib_api_v3_sdk.ApiClient(
#                 configuration
#             )
#         )
#     )

#     send_smtp_email = (
#         sib_api_v3_sdk.SendSmtpEmail(
#             to=[
#                 {
#                     "email": email
#                 }
#             ],
#             sender={
#                 "name": "Mulugu Hotel",
#                 "email": settings.FROM_EMAIL,
#             },
#             subject="Password Reset OTP",
#             html_content=f"""
#             <h2>Mulugu Hotel</h2>

#             <p>Your password reset OTP is:</p>

#             <h1>{otp}</h1>

#             <p>This OTP is valid for a limited time.</p>
#             """
#         )
#     )

#     api_instance.send_transac_email(
#         send_smtp_email
#     )

import secrets

import sib_api_v3_sdk
from django.conf import settings


def generate_otp():
    return str(
    secrets.randbelow(900000) + 100000
)


def send_otp_email(email, otp):

    configuration = sib_api_v3_sdk.Configuration()

    configuration.api_key["api-key"] = (
        settings.BREVO_API_KEY
    )

    api_instance = (
        sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(
                configuration
            )
        )
    )

    send_smtp_email = (
        sib_api_v3_sdk.SendSmtpEmail(
            to=[
                {
                    "email": email
                }
            ],
            sender={
                "name": "Mulugu Hotel",
                "email": settings.FROM_EMAIL,
            },
            subject="Password Reset OTP",
            html_content=f"""
            <h2>Mulugu Hotel</h2>

            <p>Your password reset OTP is:</p>

            <h1>{otp}</h1>

            <p>This OTP is valid for 10 minutes.</p>
            """
        )
    )

    try:
        api_instance.send_transac_email(
        send_smtp_email
    )
        return True

    except Exception:
        return False
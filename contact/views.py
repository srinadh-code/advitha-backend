from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import ContactMessage
from .serializers import ContactMessageSerializer

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException


class ContactUsView(APIView):

    def send_brevo_email(self, contact):

        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key["api-key"] = settings.BREVO_API_KEY

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )

        email = sib_api_v3_sdk.SendSmtpEmail(
            sender={
                "email": settings.FROM_EMAIL,
                "name": "Hotel Website"
            },
            to=[
                {
                    "email": settings.FROM_EMAIL
                }
            ],
            subject=f"New Contact Message from {contact.name}",
            html_content=f"""
            <h2>New Contact Message</h2>

            <p><strong>Name:</strong> {contact.name}</p>
            <p><strong>Email:</strong> {contact.email}</p>
            <p><strong>Phone:</strong> {contact.phone}</p>

            <p><strong>Message:</strong></p>
            <p>{contact.message}</p>
            """
        )

        try:
            response = api_instance.send_transac_email(email)
            print("BREVO SUCCESS:", response)
            return True

        except ApiException as e:
            print("BREVO ERROR:", e)
            return False

    def post(self, request):

        serializer = ContactMessageSerializer(data=request.data)

        if serializer.is_valid():

            contact = serializer.save()

            self.send_brevo_email(contact)

            return Response(
                {
                    "success": True,
                    "message": "Message sent successfully"
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import User


class ReceptionistContactAPIView(APIView):

    permission_classes = []

    def get(self, request):

        receptionist = User.objects.filter(
            role="receptionist"
        ).first()

        if not receptionist:
            return Response(
                {"error": "No receptionist found"},
                status=404
            )

        return Response({
            "name": f"{receptionist.first_name} {receptionist.last_name}",
            "phone_number": receptionist.phone_number,
            "email": receptionist.email,
        })
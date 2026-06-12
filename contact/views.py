
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

from .models import ContactMessage
from .serializers import ContactMessageSerializer


class ReceptionistContactAPIView(APIView):

    def get(self, request):

        enquiries = ContactMessage.objects.all().order_by(
            "-created_at"
        )

        serializer = ContactMessageSerializer(
            enquiries,
            many=True
        )

        return Response(serializer.data)
    
class ReplyContactAPIView(APIView):

    def post(self, request, enquiry_id):

        try:
            enquiry = ContactMessage.objects.get(id=enquiry_id)
        except ContactMessage.DoesNotExist:
            return Response(
                {"error": "Enquiry not found"},
                status=404
            )

        subject = request.data.get("subject")
        message = request.data.get("message")

        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key["api-key"] = settings.BREVO_API_KEY

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )

        email = sib_api_v3_sdk.SendSmtpEmail(
            sender={
                "email": settings.FROM_EMAIL,
                "name": "Mulugu Hotel"
            },
            to=[
                {
                    "email": enquiry.email,
                    "name": enquiry.name
                }
            ],
            subject=subject,
            html_content=f"""
            <p>Dear {enquiry.name},</p>

            <p>{message}</p>

            <br>

            <p>Regards,</p>
            <p>Mulugu Hotel Team</p>
            """
        )

        try:
            api_instance.send_transac_email(email)

            enquiry.status = "replied"
            enquiry.save()

            return Response({
                "success": True,
                "message": "Reply sent successfully"
            })

        except ApiException as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
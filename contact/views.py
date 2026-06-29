


from django.conf import settings
from django.utils.html import escape
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import ContactMessage
from .serializers import ContactMessageSerializer
from accounts.models import User

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

logger = logging.getLogger(__name__)



# Customer Contact Form

class ContactUsView(APIView):

    def send_brevo_email(self, contact):
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key["api-key"] = settings.BREVO_API_KEY

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )

        # Latest receptionist
        receptionist = User.objects.filter(
            role="receptionist"
        ).order_by("-id").first()

        

        if receptionist:
            receiver_email = receptionist.email
        else:
            logger.warning(
        "No receptionist found, sending contact email to FROM_EMAIL."
        )
            receiver_email = settings.FROM_EMAIL

        email = sib_api_v3_sdk.SendSmtpEmail(
            sender={
                "email": settings.FROM_EMAIL,
                "name": "Hotel Website"
            },
            to=[
                {
                    "email": receiver_email
                }
            ],
            subject=f"New Contact Message from {contact.name}",
           
            html_content=f"""
<h2>New Contact Message</h2>

<p><strong>Name:</strong> {escape(contact.name)}</p>
<p><strong>Email:</strong> {escape(contact.email)}</p>
<p><strong>Phone:</strong> {escape(contact.phone)}</p>

<p><strong>Message:</strong></p>
<p>{escape(contact.message)}</p>
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

            if not self.send_brevo_email(contact):
                return Response(
                {
                    "success": False,
                    "message": "Message saved but email could not be sent."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

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



# Contact Page Info

class ReceptionistContactAPIView(APIView):

    def get(self, request):
        receptionist = User.objects.filter(
            role="receptionist"
        ).order_by("-id").first()

        if not receptionist:
            return Response({
                "phone_number": None,
                "email": None
            })

        return Response({
            "email": receptionist.email,
            "phone_number": receptionist.phone_number
        })




class ReceptionistEnquiriesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role not in ["admin", "receptionist"]:
            return Response(
                {"error": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN
            )

        enquiries = ContactMessage.objects.all().order_by("-created_at")
        serializer = ContactMessageSerializer(enquiries, many=True)
        return Response(serializer.data)



# Reply to Customer

class ReplyContactAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, enquiry_id):
        if request.user.role not in ["admin", "receptionist"]:
            return Response(
            {"error": "Permission denied."},
            status=status.HTTP_403_FORBIDDEN
        )

        try:
            enquiry = ContactMessage.objects.get(id=enquiry_id)
        except ContactMessage.DoesNotExist:
            return Response(
                {"error": "Enquiry not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        subject = request.data.get("subject")
        message = request.data.get("message")
        if not subject or not subject.strip():
            return Response(
            {
                "error": "Subject is required."},
            status=status.HTTP_400_BAD_REQUEST
            )

        if not message or not message.strip():
            return Response(
                {
                    "error": "Message is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

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
        <p>Dear {escape(enquiry.name)},</p>

        <p>{escape(message)}</p>

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
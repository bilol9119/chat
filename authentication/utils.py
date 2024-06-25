import re
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
import random


def otp_code_generator():
    return random.randint(10000, 99999)


def validate_password(string):
    pattern = (
        r'^(?=.*[a-z])'  # At least one lowercase letter
        r'(?=.*\d)'  # At least one digit
        r'[A-Za-z\d@$!%*?&]{8,}$'  # Allowed characters and at least 8 characters long
    )
    if not re.match(pattern, string):
        return False
    return True


def send_otp_via_email(email, otp_code):
    subject = "Code for one time registration!"
    message = f"Your code is {otp_code}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    connection = get_connection(host=settings.EMAIL_HOST,
                                port=settings.EMAIL_PORT,
                                username=settings.EMAIL_HOST_USER,
                                password=settings.EMAIL_HOST_PASSWORD,
                                use_tls=settings.EMAIL_USE_TLS)
    email_message = EmailMessage(
        subject, message, email_from, recipient_list, connection=connection
    )

    # Sending the email and catching potential exceptions
    try:
        email_message.send()
        return True
    except Exception as e:
        print(f"Error sending OTP: {e}")
        return False

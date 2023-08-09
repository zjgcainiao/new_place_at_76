from django.shortcuts import render, redirect
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from django.contrib import messages
import requests
import os
from dotenv import load_dotenv
import json


# load_dotenv()  # take environment variables from .env.


# added on 2023-06-01 to validate if a receipent email is valid.
# using abstractapi.com's email validation.
# https://www.abstractapi.com/guides/django-send-email#:~:text=In%20order%20to%20send%20emails,and%20generate%20an%20app%20password.

# response = requests.get("https://emailvalidation.abstractapi.com/v1/?api_key=42274badcea24851ac408a1da8f79bda&email=info@76prolubeplus.com")
# print(response.status_code)
# print(response.content)
api_key = os.environ.get('EMAIL_VERIFICATION_API_KEY')
api_url = 'https://emailvalidation.abstractapi.com/v1/?api_key=' + api_key


def is_valid_email(data):
    if data['is_valid_format']['value'] and data['is_mx_found']['value'] and data['is_smtp_valid']['value']:
        if data['is_role_email']['value']:
            return True
    return False


def validate_email(email):
    email_url = '&email=' + email
    response = requests.get(api_url + email_url)
    # Decode the byte string into a regular string
    content_str = response.content.decode('utf-8')
    # Convert the string to a JSON object
    content_json = json.loads(content_str)
    is_valid = is_valid_email(content_str)
    return is_valid


# Create your views here.
def send_email_sample(request):
    if request.method == "POST":
        with get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS
        ) as connection:

            subject = request.POST.get("subject")
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST.get("email"), ]
            message = request.POST.get("message")
            messages.add_message(request, messages.SUCCESS,
                                 f"email has been sent to {recipient_list}")
            EmailMessage(subject, message, email_from,
                         recipient_list, connection=connection).send()
            # return redirect('automatic_mails/email_sent_success.html')
            return render(request, 'automatic_mails/email_sent_success.html')

    return render(request, 'automatic_mails/send_an_email.html')

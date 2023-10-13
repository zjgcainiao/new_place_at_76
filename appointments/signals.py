from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from appointments.models import AppointmentRequest
from django.template.loader import render_to_string
import logging
from django.core.mail import EmailMessage, get_connection
from urllib.parse import urljoin
from django.conf import settings
from django.urls import reverse_lazy, reverse


logger = logging.getLogger('django')


@receiver(post_save, sender=AppointmentRequest)
def send_appointment_confirmation_email(sender, instance, created, **kwargs):
    if created:

        mail_subject = "Appointment Confirmation"
        appointment = instance

        logger.info(
            f'sending appointment confirmation email to {appointment.appointment_email}. Appointment Confirmation Id is: {appointment.appointment_confirmation_id}')

        context = {
            'appointment_confirmation_id': instance.appointment_confirmation_id,
            'email': instance.appointment_confirmation_id,
            'appointment': instance,
        }

        try:

            with get_connection(
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=settings.EMAIL_HOST_USER,
                password=settings.EMAIL_HOST_PASSWORD,
                use_tls=settings.EMAIL_USE_TLS,
            ) as connection:

                subject = mail_subject
                email_from = settings.EMAIL_HOST_USER
                message = render_to_string(
                    'appointments/10_new_appointment_email.html', context)
                recipient_list = [appointment.appointment_email, ]

                # Modify recipient_list if "testing" or "test" is present in any email
                if any('testing' in email or 'test' in email or '22-' in email in email for email in recipient_list):
                    recipient_list = ['holleratme420@gmail.com']

                email = EmailMessage(subject, message, email_from,
                                     recipient_list,
                                     connection=connection)

                email.content_subtype = "html"
                sent_count = email.send()

                if sent_count:
                    logger.info(
                        f"email has been sent to {recipient_list} successfully.")
                else:
                    logger.error(
                        f"failed to send email to {recipient_list}.")

                # this is required because the main content is now HTML
                #  email.content_subtype = "html"
                # email.send()
            # send_mail(
            #     'Welcome to Amazing Automan company platform',
            #     f'Hello {instance.talent_first_name}, your temporary password is: {random_password}. Please change it on your first login.',
            #     settings.DEFAULT_FROM_EMAIL,
            #     [instance.talent_email],
            #     fail_silently=False,
            # )
        except Exception as e:
            # Handle email sending errors if needed, e.g., logging the error.
            print(f"Error sending email: {e}")
            logger.error(f"Error sending email: {e}")

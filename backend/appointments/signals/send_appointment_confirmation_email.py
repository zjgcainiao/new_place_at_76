from .base import models, \
            settings, get_connection, render_to_string, post_save, receiver, \
             AppointmentRequest, EmailMessage, \
            SMTPException, SMTPAuthenticationError, SMTPServerDisconnected, BadHeaderError, \
            timezone, logger, settings

from django.contrib.sites.models import Site
from django.urls import reverse

@receiver(post_save, sender=AppointmentRequest)
def send_appointment_confirmation_email(sender, instance, created, **kwargs):
    if created:
        mail_subject = "Appointment Request Received."
        appointment = instance
        
        # Get current site domain dynamically
        if settings.DEBUG:
            domain = '127.0.0.1:8000'  # Development domain
        else:
            current_site = Site.objects.get_current()
            domain = current_site.domain  # Production domain

        # Determine the protocol based on the DEBUG setting
        protocol = 'http' if settings.DEBUG else 'https'

        # Determine the protocol based on the DEBUG setting
        protocol = 'http' if settings.DEBUG else 'https'

        # Generate the absolute URL
        appointment_detail_path = reverse('appointments:appointment_detail_by_confirmation', 
                                          kwargs={'appointment_confirmation_id': appointment.appointment_confirmation_id})
        appointment_detail_url = f'{protocol}://{domain}{appointment_detail_path}'

        logger.info(
            f"sending appointment confirmation email to {appointment.appointment_email}. \
                Appointment Confirmation Id is: {appointment.appointment_confirmation_id}")

        context = {
            'appointment_confirmation_id': instance.appointment_confirmation_id,
            'email': instance.appointment_email,
            'appointment': instance,
            'appointment_detail_url': appointment_detail_url,  # Use this in the template
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
                    'appointments/40_new_appointment_email_template.html', context)
                recipient_list = [appointment.appointment_email ]

                # Modify recipient_list if "testing" or "test" is present in any email
            if any(substring in email.lower() for substring in ['testing', 'test', '22-'] for email in recipient_list):
                recipient_list = ['holleratme420@gmail.com']
                email = EmailMessage(subject, message, 
                                     email_from,
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

            # )
        except (SMTPException, SMTPAuthenticationError, SMTPServerDisconnected) as smtp_error:
            logger.error(f"SMTP error occurred: {smtp_error}", exc_info=True)
        except BadHeaderError as bad_header_error:
            logger.error(f"Bad header found: {bad_header_error}", exc_info=True)
        except Exception as general_error:
            logger.error(f"An unexpected error occurred when sending email: {general_error}", exc_info=True)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from customer_users.models import CustomerUser
from internal_users.models import InternalUser
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, get_connection
from django.template.loader import render_to_string
import logging
from urllib.parse import urljoin
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from customer_users.token_generators import decode_activation_token_for_customer_user,create_activation_token_for_customer_user

# logger. use standard 'django.db' level logging.
logger = logging.getLogger('django.db')

# sending activation emails for newly created customer users
@receiver(post_save, sender=CustomerUser)
def generate_new_account_email(sender, instance, created, **kwargs):
    if created:
            user = instance
            mail_subject = 'Activate Your New Account'
            # Generate token using pyJWT
            token = create_activation_token_for_customer_user(user)
            # token = account_activation_token.make_token(internal_user)
            print(
                f'the token just generated for new customer user id {user.pk} and it is {token}')
            logger.info(
                f'the token just generated for new customer user id {user.pk} and it is {token}')

            def get_protocol(domain):
                if domain in ["localhost", "127.0.0.1:8000"]:
                    return "http"
                else:
                    return "https"

            # manul setup the domain for testing
            domain = 'new76prolubeplus.com' #'127.0.0.1:8000'  # 'new76prolubeplus.com', '127.0.0.1:8000'
            # Construct activation link
            # domain = get_current_site(None).domain
            protocol = get_protocol(domain)
            # code the primary key pk with base64

            relative_link = reverse(
                'customer_users:activate_customer_user_account', args=[token])
            activation_link = urljoin(f"{protocol}://{domain}/", relative_link)
            print(f'the activation_link is {activation_link}.')
            logger.info(f'the activation_link is {activation_link}.')
            context = {
                'cust_user_first_name': user.cust_user_first_name,
                'cust_user_id':instance.pk,
                # Replace with your actual activation link logic
                'activation_link': activation_link,
            }
            try:

                with get_connection(
                    host=settings.EMAIL_HOST,
                    port=settings.EMAIL_PORT,
                    username=settings.EMAIL_HOST_USER,
                    password=settings.EMAIL_HOST_PASSWORD,
                    use_tls=settings.EMAIL_USE_TLS
                ) as connection:

                    subject = mail_subject
                    email_from = settings.EMAIL_HOST_USER
                    message = render_to_string(
                        'customer_users/10_customer_user_registration_email.html', context)
                    recipient_list = [user.cust_user_email,]

                    # Modify recipient_list if "testing" or "test" is present in any email
                    if any('testing' in email.lower() or 'test' in email.lower() for email in recipient_list):
                        logging.info('testing email address detected...redirecting to holleratme420@gmail.com...')
                        recipient_list = ['holleratme420@gmail.com']

                    email = EmailMessage(subject, message, email_from,
                                         recipient_list,
                                         connection=connection)

                    email.content_subtype = "html"
                    sent_count = email.send()

                    if sent_count:
                        logger.info(
                            f"activation email for customer user {instance.pk} has been sent to {recipient_list} successfully.")
                    else:
                        logger.error(
                            f"failed to send email to {recipient_list}.")

            except Exception as e:
                # Handle email sending errors if needed, e.g., logging the error.
                print(f"Error sending customer user activation email: {e}")
                logger.error(f"Error sending customer user activation email: {e}")
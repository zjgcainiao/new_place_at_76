from .base import receiver, post_save, TalentsModel, InternalUser, \
                create_activation_token, reverse_lazy, reverse, \
                urljoin, get_connection, settings, render_to_string, EmailMessage, logger, settings

@receiver(post_save, sender=TalentsModel)  # sender='talent_management.Talent'
def create_internal_user(sender, instance, created, **kwargs):
    if created:
        if not InternalUser.objects.filter(email=instance.talent_email).exists():
            # Generate a random password
            random_password = InternalUser.objects.make_random_password()

            # Create a new InternalUser instance with data from Talent instance
            # technically, it should allow one talent email to have mutiple internal user accounts.
            internal_user = InternalUser.objects.create(
                user_first_name=instance.talent_first_name.strip().capitalize(),
                user_last_name=instance.talent_last_name.strip().capitalize(),
                user_talent=instance,
                email=instance.talent_email,
                user_is_active=False,  # set it as false before activating
            )
            # Hash and set the password
            internal_user.set_password(random_password)
            internal_user.save()
            logger.info(
                f'creating new internal user profile. Using new talent_email: {internal_user.email}. Internal User ID is: {internal_user.pk}. Activation is required.')
            # Send the user an email with the temporary password

            # Render the email content from the template
            mail_subject = 'Activate your employee user account'

            # Generate token using pyJWT
            token = create_activation_token(internal_user)
            # old token generation mehod: PasswordResetHashGenerator
            # token = account_activation_token.make_token(internal_user)

            logger.info(
                f'the token just generated for new internal user id {internal_user.pk} and about to be sent via activation link is {token}')

            def get_protocol(domain):
                if domain in ["localhost", "127.0.0.1:8000"]:
                    return "http"
                else:
                    return "https"

            # manul setup the domain for testing
            if settings.DEBUG:
                domain = '127.0.0.1:8000'
            else:
                domain = 'new76prolubeplus.com' 
            # Construct activation link
            # domain = get_current_site(None).domain
            protocol = get_protocol(domain)
            # code the primary key pk with base64
            # encoded_pk = urlsafe_base64_encode(force_bytes(internal_user.pk))
            relative_link = reverse(
                'internal_users:activate_internal_user_account', args=[token])
            # activation_link = f"https://{domain}/{relative_link}"
            activation_link = urljoin(f"{protocol}://{domain}/", relative_link)
            logger.info(f'The activation_link is {activation_link}.')
            context = {
                'user_first_name': internal_user.user_first_name,
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
                        'talent_management/80_new_internal_user_activation_email.html', context)
                    recipient_list = [internal_user.email,]

                    # Modify recipient_list if "testing" or "test" is present in any email
                    if any('testing' in email or 'test' in email for email in recipient_list):
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


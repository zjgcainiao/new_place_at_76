# this file incldues the signals related to creating, updating and deleting an employee record
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from talent_management.models import TalentsModel
from internal_users.models import InternalUser

from django.contrib.auth.models import User
# @receiver(post_save, sender=TalentsModel)
# def send_invite_email(sender, instance, created, **kwargs):
#     if created:
#         subject = 'Invitation to register as an InternalUser'
#         message = f'Hi {instance.talent_first_name},\n\nYou have been invited to register as an InternalUser. Please click the following link to register:\n\n{settings.BASE_URL}/register/?email={instance.email}\n\nThanks,\nThe InternalUser team'
#         send_mail(subject, message, settings.EMAIL_HOST_USER, [instance.email], fail_silently=False)


# 2023-05-23 when creating a new employee record, a new internal_user shall be created
# this one shall be tested after talent creation page is finished

@receiver(post_save, sender=TalentsModel) #sender='talent_management.Talent'
def create_internal_user(sender, instance, created, **kwargs):
    if created:
        # Create a new InternalUser instance with data from Talent instance
        InternalUser.objects.create(
            user_first_name=instance.talent_first_name,
            user_last_name=instance.talent_last_name,
            user_talent_id=instance.talent_id,
            email=instance.talent_email,
            password='temporary_password'  # Replace with actual temporary password generation logic
            # password = InternalUser.objects.make_random_password()
        )
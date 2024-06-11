# Use this task in your signal or view
from tasks import process_customer_from_appointment_task
from django.db.models.signals import post_save
from django.dispatch import receiver
from appointments.models import AppointmentRequest
import logging

logger = logging.getLogger('management_scripts')


@receiver(post_save, sender=AppointmentRequest)
def process_customer_from_appointment_signal(sender, instance,
                                             created, **kwargs):
    logger.info(f"Processing customer info from a new appointment: {instance}")
    if created:
        process_customer_from_appointment_task.delay(instance.id)

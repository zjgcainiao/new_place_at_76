from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from shift_management.models import Shift
from shift_management.models import AuditHistory
from shift_management.tasks import add_audit_history_record
from django.contrib.contenttypes.models import ContentType
import logging
logger=logging.getLogger('django.db')

# @receiver(post_save, sender=Shift)
# def create_update_shift_handler(sender, instance, created, **kwargs):
#     if created:
#         action = 'created'
#     else:
#         action = 'updated'
    
#     AuditHistory.objects.create(
#         action=action,
#         changed_by=instance.modified_by,  # Assuming `modified_by` is updated whenever a shift is changed
#         description=f"Shift {action}: {instance}",
#         content_object=instance
#     )


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from shift_management.models import Shift
from shift_management.models import AuditHistory
from shift_management.tasks import add_audit_history_record
from django.contrib.contenttypes.models import ContentType
import logging
logger=logging.getLogger('django.db')
# trigger the Celery tasks instead of directly performing the operations.
@receiver(post_save, sender=Shift)
def create_update_shift_handler(sender, instance, created, **kwargs):
    logger.info("create_update_shift_handler signal triggered: instance={}, created={}".format(instance, created))

    action = 'created' if created else 'updated'
    content_type = ContentType.objects.get_for_model(instance)
    add_audit_history_record.delay(
        action, 
        instance.modified_by, 
        f"Shift {action}: {instance.id}", 
        instance.id,
        content_type,
        # content_type.id  # Passing the ID of the ContentType instance 
    )

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

# @receiver(post_delete, sender=Shift)
# def delete_shift_handler(sender, instance, **kwargs):
#     AuditHistory.objects.create(
#         action='deleted',
#         changed_by=instance.modified_by,  # You might need to adjust this depending on how you handle deletions
#         description=f"Shift deleted: {instance}",
#         content_object=instance
#     )

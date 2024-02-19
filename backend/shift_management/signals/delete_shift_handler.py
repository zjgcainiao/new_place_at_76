from .base import logger, add_audit_history_record, post_save, Shift, ContentType, receiver, post_delete
from shift_management.models import AuditHistory

@receiver(post_delete, sender=Shift)
def delete_shift_handler(sender, instance, **kwargs):
    AuditHistory.objects.create(
        action='deleted',
        changed_by=instance.modified_by,  # You might need to adjust this depending on how you handle deletions
        description=f"Shift deleted: {instance}",
        content_object=instance
    )

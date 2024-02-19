from .base import logger, add_audit_history_record, post_save, Shift, ContentType, receiver

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

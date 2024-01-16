import logging
from celery import shared_task
from shift_management.models import AuditHistory

logger = logging.getLogger('django.db')

@shared_task
def add_audit_history_record(action, user_id, description, object_id, instance, content_type_id):
    AuditHistory.objects.create(
        action=action,
        modified_by=user_id,
        description=description,
        object_id=object_id,
        content_object=instance,
        content_type_id=content_type_id
    )
    logger.info("Audit history record created: action={}, user_id={}, description={}, object_id={}, content_type_id={}".format(
        action, user_id, description, object_id, content_type_id))

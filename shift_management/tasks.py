import logging
from celery import shared_task
from shift_management.models import AuditHistory
from django.contrib.contenttypes.models import ContentType

logger = logging.getLogger('django.db')

@shared_task
def add_audit_history_record(action, user_id, description, object_id, content_type):
        # Create the audit history record
    try:
        audit_record = AuditHistory.objects.create(
                action=action,
                modified_by_id=user_id,
                description=description,
                object_id=object_id,
                content_type=content_type
            )

        logger.info("Audit history record created: action={}, user_id={}, description={}, object_id={}, content_type={}".format(
            action, user_id, description, object_id, content_type))
    except ContentType.DoesNotExist:
            logger.error(f"ContentType with id {content_type.id} does not exist.")
    except Exception as e:
            # Log any other exception that might occur
            logger.exception(f"Failed to create audit history record: {e}")
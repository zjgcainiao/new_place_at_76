from celery import shared_task
from shift_management.models import AuditHistory

@shared_task
def add_audit_history_record(action, user_id, description, object_id, content_type_id):
    AuditHistory.objects.create(
        action=action,
        changed_by_id=user_id,
        description=description,
        object_id=object_id,
        content_type_id=content_type_id
    )

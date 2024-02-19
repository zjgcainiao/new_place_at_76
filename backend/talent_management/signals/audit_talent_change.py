from .base import receiver, post_save, TalentsModel, TalentAudit, logger, timezone
from django.db import transaction

@receiver(post_save, sender=TalentsModel)
def audit_talent_changes(sender, instance, **kwargs):
    # Check if the instance has the specific fields changed
    # This requires the use of instance._changed_fields or similar logic
    # Assuming that _changed_fields is a dictionary with field names as keys
    # and their previous values as values
    logger.debug("Audit talent changes triggered for instance: %s", instance)
    changed_fields = instance.get_changed_fields()
    if not changed_fields:
        return
    with transaction.atomic():
        for field, old_value in changed_fields.items():
            # For instance, if talent_pay_rate changed:

            TalentAudit.objects.create(
                talent=instance,
                # Assuming you have a method or field on Talents that holds the current user making the change
                created_by=instance.updated_by_user,
                created_at=timezone.now(),
                field_changed=field,
                old_value=old_value,
                new_value=getattr(instance, field),
            )

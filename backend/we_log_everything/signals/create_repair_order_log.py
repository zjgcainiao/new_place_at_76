from django.db.models.signals import post_save
from django.dispatch import receiver
from homepageapp.models import RepairOrdersNewSQL02Model as RepairOrder
from we_log_everything.models import RepairOrderLog
from django.contrib.contenttypes.models import ContentType


@receiver(post_save, sender=RepairOrder)
def create_repair_order_log(sender, instance, created, **kwargs):
    action = 'Created' if created else 'Updated'
    description = f"RepairOrder with ID {instance.id} was {action}."

    RepairOrderLog.objects.create(
        action=action,
        description=description,
        content_type=ContentType.objects.get_for_model(instance),
        object_id=instance.id
    )

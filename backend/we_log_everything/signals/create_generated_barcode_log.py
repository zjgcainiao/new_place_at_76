from django.db.models.signals import post_save
from django.dispatch import receiver
from httpx import post
from core_operations.models import GeneratedBarCode
from we_log_everything.models import DataModelChangeLog, CHANGE_LOG_ACTION_CHOICES

# DataModelChangeLog is a model that logs all changes across multiple models. I use GeneratedBarCode to demonstrate how to log changes in a model.
@receiver(post_save, sender=GeneratedBarCode)
def create_generated_barcode_log(sender, instance, created, **kwargs):
   
    if created:
        DataModelChangeLog.objects.create(
            content_object=instance,
            description=f"GeneratedBarCode with ID {instance.id} was Created.",
            new_value=instance.full_code,
            field_changed='full_code',
            old_value=None,
            action=CHANGE_LOG_ACTION_CHOICES[0][0],

        )
    else:
        # check for changes in any field by looking into the tracker
        tracker = instance.tracker
        for field in tracker.changed():
            old_value = tracker.previous(field)
            new_value = getattr(instance, field)
            DataModelChangeLog.objects.create(
                content_object=instance,
                description=f"GeneratedBarCode with ID {instance.id} was Updated.",
                new_value=new_value,
                old_value=old_value,
                field_changed=field,
                action=CHANGE_LOG_ACTION_CHOICES[1][0],
            )
from re import A
from tabnanny import verbose
from .base import models, InternalUser, CustomerUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Path: backend/we_log_everything/models/data_model_log.py

CHANGE_LOG_ACTION_CHOICES = [
    ('Created', 'Created'),
    ('Updated', 'Updated'),
    ('Deleted', 'Deleted'),
    ('Restored', 'Restored'),
    ('Other', 'Other'),
]


class DataModelChangeLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    # a category of actions while `description` describes the specific detail
    action = models.CharField(
        max_length=255, choices=CHANGE_LOG_ACTION_CHOICES)
    description = models.TextField()
    description_in_json = models.JSONField(null=True, blank=True)
    field_changed = models.CharField(max_length=255, null=True, blank=True)
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)

    # Fields to link to any Django model
    content_type = models.ForeignKey(
        ContentType, on_delete=models.DO_NOTHING, null=True, blank=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Data Model Change Log'
        verbose_name_plural = 'Data Model Change Logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"Log for Object ID {self.object_id} - {self.action} at {self.created_at: %Y-%m-%d %H:%M}"

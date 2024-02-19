from .base import models, InternalUser, TalentsModel, timedelta, ContentType, GenericForeignKey

class AuditHistory(models.Model):
    """
    Represents the audit history of a model instance.

    Each instance of this model represents a specific action performed on a tracked model,
    such as creation, update, or deletion. It stores information about the action, the user
    who performed it, the timestamp, and a description.

    Attributes:
        action (str): The action performed on the tracked model.
        changed_by (User): The user who performed the action.
        timestamp (datetime): The timestamp when the action was performed.
        description (str): A description of the action.
        content_type (ContentType): The content type of the tracked model.
        object_id (int): The ID of the tracked model instance.
        content_object (Model): The tracked model instance.

    Methods:
        __str__(): Returns a string representation of the audit history entry.

    Meta:
        ordering (list): The default ordering for audit history entries based on the timestamp.
    """
    AUDIT_HISTORY_ACTION_CHOICES = [
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted')
    ]

    action = models.CharField(max_length=10, choices=AUDIT_HISTORY_ACTION_CHOICES)
    modified_by = models.ForeignKey(InternalUser, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)

    # ForeignKeys to different models being tracked, use GenericForeignKey for more flexibility
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.get_action_display()} by {self.changed_by} on {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']

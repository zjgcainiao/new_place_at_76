from .base import models, InternalUser

class OperatorNotification(models.Model):
    operator = models.ForeignKey(
        InternalUser, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='operator_notifications')
    message = models.CharField(max_length=255, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'operator_notifications'
        ordering = ["-created_at",]
        verbose_name = 'Operator Notification'
        verbose_name_plural = 'Operator Notifications'
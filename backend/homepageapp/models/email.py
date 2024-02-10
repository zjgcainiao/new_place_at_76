from .base import models, InternalUser


class EmailsNewSQL02Model(models.Model):
    email_id = models.IntegerField(primary_key=True)
    email_type_id = models.IntegerField()
    email_address = models.EmailField()
    email_description = models.CharField(max_length=255, null=True, blank=True)
    email_can_send_notification = models.BooleanField(default=True)
    email_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='email_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='email_modified', on_delete=models.SET_NULL, null=True, blank=True)
    email_last_updated_at = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'emails_new_03'
        ordering = ["-email_id"]
        verbose_name = 'email'
        verbose_name_plural = 'emails'


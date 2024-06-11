from operator import index
from .base import models, InternalUser
from django.db.models import Max
from django.db import transaction
class EmailsNewSQL02Model(models.Model):
    email_id = models.IntegerField(primary_key=True)
    email_type_id = models.IntegerField(default=1)
    email_address = models.EmailField()
    email_description = models.CharField(max_length=255, null=True, blank=True)
    email_can_send_notification = models.BooleanField(default=True)
    email_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='email_created', on_delete=models.SET_NULL, 
        null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='email_modified', on_delete=models.SET_NULL, null=True, blank=True)
    email_last_updated_at = models.DateTimeField(auto_now=True, null=True)

    @property
    def get_cleaned_email_address(self):
        return self.email_address.strip().lower()

    def save(self, *args, **kwargs):
        # manual iteration to get the max email_id
        if not self.email_id:  # Check if it's a new instance
            with transaction.atomic():  # Ensure the operation is atomic
                # Get the current maximum email_id
                current_max_id = EmailsNewSQL02Model.objects.aggregate(max_id=Max('email_id'))['max_id']
                # If there are no entries yet, start with 1
                self.email_id = (current_max_id or 0) + 1
        if self.email_address:
            self.email_address = self.email_address.strip().lower()
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'emails_new_03'
        ordering = ["-email_id"]
        verbose_name = 'email'
        verbose_name_plural = 'emails'


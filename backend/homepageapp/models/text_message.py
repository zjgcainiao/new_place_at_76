from .base import models, InternalUser
from .customer import CustomersNewSQL02Model


class TextMessagesModel(models.Model):
    text_message_id = models.AutoField(primary_key=True)
    text_customer = models.ForeignKey(
        CustomersNewSQL02Model, on_delete=models.SET_NULL, null=True, related_name='text_customers')
    text_body = models.CharField(max_length=4000, blank=True, null=True)
    text_external_id = models.BigIntegerField(null=True, blank=True)
    text_type = models.IntegerField()
    text_to_phonenumber = models.CharField(max_length=15)
    text_direction = models.BooleanField(default=False)
    text_status = models.IntegerField(null=True, blank=True)
    text_error_message = models.CharField(
        max_length=255, null=True, blank=True)
    text_error_code = models.CharField(max_length=255, null=True, blank=True)
    text_datetime = models.DateTimeField(null=True, blank=True)
    text_body_size = models.IntegerField(null=True, blank=True)
    text_created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='text_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='text_modified', on_delete=models.SET_NULL, null=True, blank=True)
    text_last_updated_at = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'textmessages_new_03'
        ordering = ['-text_message_id']
        verbose_name = 'textmessage'
        verbose_name_plural = 'textmessages'

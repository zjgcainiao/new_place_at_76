from .base import models, InternalUser
from .customer import CustomersNewSQL02Model
from .email import EmailsNewSQL02Model

class CustomerEmailsNewSQL02Model(models.Model):
    customeremail_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        CustomersNewSQL02Model, on_delete=models.CASCADE)
    email = models.ForeignKey(EmailsNewSQL02Model, on_delete=models.CASCADE)
    customeremail_is_selected = models.BooleanField(default=True)

    customeremail_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='customeremail_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='customeremail_modified', on_delete=models.SET_NULL, null=True, blank=True)
    customeremail_last_updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'customeremails_new_03'
        ordering = ["-customeremail_id", '-email']
        # verbose_name = 'customeremail'
        # verbose_name_plural = 'customeremails'
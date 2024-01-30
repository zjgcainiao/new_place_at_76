from django.db import models
from internal_users.models import InternalUser

class AccountClassModel(models.Model):
    account_class_id = models.AutoField(primary_key=True)
    account_type = models.CharField(max_length=30, null=True)
    account_last_updated_at = models.DateTimeField(auto_now=True, null=True)
    account_created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='accountclass_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='accountclass_modified', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'accountclasses_new_03'
        ordering = ["-account_class_id"]
        verbose_name = 'accountclass'
        verbose_name_plural = 'accountclasses'

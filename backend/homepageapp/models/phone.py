from .base import models, InternalUser, FormattedPhoneNumberField
from .phone_desc import PhoneDescModel
import re

class PhonesNewSQL02Model(models.Model):
    phone_id = models.AutoField(primary_key=True)
    phone_desc = models.ForeignKey(
        PhoneDescModel, on_delete=models.SET_NULL, null=True, related_name='phone_descs')
    phone_number = models.CharField(max_length=20)
    phone_number_digits_only = models.CharField(
        max_length=20, null=True, blank=True)
    phone_number_ext = models.CharField(max_length=10, blank=True, null=True)
    phone_displayed_name = models.CharField(max_length=100)
    phone_memo_01 = models.TextField(blank=True, null=True)
    phone_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='phone_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='phone_modified', on_delete=models.SET_NULL, null=True, blank=True)
    phone_last_updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_phone_number_digit_only(self):
        phone_number_digits = re.sub(r'\D', '', self.phone_number)

    # custom the corresponding data table name for this model
    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'phones_new_03'
        ordering = ["-phone_id"]
        verbose_name = 'phone'
        verbose_name_plural = 'phones'

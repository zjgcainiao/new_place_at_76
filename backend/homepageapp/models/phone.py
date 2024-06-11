from .base import models, InternalUser, FormattedPhoneNumberField
from .phone_desc import PhoneDescModel
import re
from core_operations.constants import US_COUNTRY_CODE


class PhonesNewSQL02Model(models.Model):
    phone_id = models.AutoField(primary_key=True)
    phone_desc = models.ForeignKey(
        PhoneDescModel, on_delete=models.SET_NULL, null=True,
        related_name='phone_descs')
    phone_number_country_code = models.CharField(
        max_length=5, blank=True, null=True,
        default=US_COUNTRY_CODE)
    phone_number = models.CharField(max_length=20)
    phone_number_digits_only = models.CharField(
        max_length=20, null=True, blank=True)
    phone_number_ext = models.CharField(max_length=10, blank=True, null=True)
    phone_displayed_name = models.CharField(max_length=100)
    phone_memo_01 = models.TextField(blank=True, null=True)
    phone_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='phone_created',
        on_delete=models.DO_NOTHING,
        null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='phone_modified',
        on_delete=models.DO_NOTHING,
        null=True, blank=True)
    phone_last_updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_phone_number_digits(self):
        phone_number_digits = re.sub(r'\D', '', self.phone_number)
        return phone_number_digits

    # savs the phone number in digits only
    def save(self, *args, **kwargs):
        self.phone_number_digits_only = self.get_phone_number_digits
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'phones_new_03'
        ordering = ["-phone_id"]
        verbose_name = 'Phone'
        verbose_name_plural = 'Phones'

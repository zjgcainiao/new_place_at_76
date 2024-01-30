from django.db import models
from internal_users.models import InternalUser

class AddressesNewSQL02Model(models.Model):
    address_id = models.AutoField(primary_key=True)
    address_type_id = models.IntegerField()
    address_company_or_ATTN = models.CharField(
        max_length=50, null=True, blank=True)
    address_line_01 = models.CharField(max_length=80, null=True, blank=True)
    address_city = models.CharField(max_length=50,  null=True, blank=True)
    address_state = models.CharField(max_length=50, null=True, blank=True)
    address_zip_code = models.CharField(max_length=30, null=True, blank=True)
    address_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='address_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='address_modified', on_delete=models.SET_NULL, null=True, blank=True)
    address_last_updated_at = models.DateTimeField(auto_now=True, null=True)

    @property
    def get_full_address(self):
        addr_fields = [self.address_line_01, self.address_city, self.address_state.upper(),
                       self.address_zip_code]

        full_address = " ".join(
            [field for field in addr_fields if field is not None]).strip()

        return full_address

    @property
    def get_full_address_with_ATTN(self):
        addr_fields = [self.address_company_or_ATTN, self.address_line_01, self.address_city, self.address_state.upper(),
                       self.address_zip_code]

        full_address = " ".join(
            [field for field in addr_fields if field is not None]).strip()

        return full_address

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'addresses_new_03'
        ordering = ["-address_id"]
        verbose_name = 'address'
        verbose_name_plural = 'addresses'
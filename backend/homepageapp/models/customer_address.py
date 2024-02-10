from .base import models, InternalUser
from .address import AddressesNewSQL02Model
from .customer import CustomersNewSQL02Model


class CustomerAddressesNewSQL02Model(models.Model):
    address = models.ForeignKey(
        AddressesNewSQL02Model, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        CustomersNewSQL02Model, on_delete=models.CASCADE)

    customeraddress_created_at = models.DateTimeField(
        auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='customeraddress_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='customeraddress_modified', on_delete=models.SET_NULL, null=True, blank=True)
    customeraddress_last_updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'customeraddresses_new_03'
        ordering = ["-address", '-customer']
        # verbose_name = 'customeraddress'
        # verbose_name_plural = 'customeraddresses'

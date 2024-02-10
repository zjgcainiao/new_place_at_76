from .base import models, InternalUser, FormattedPhoneNumberField
from .phone import PhonesNewSQL02Model
from .customer import CustomersNewSQL02Model

class CustomerPhonesNewSQL02Model(models.Model):
    phone = models.ForeignKey(PhonesNewSQL02Model, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        CustomersNewSQL02Model, on_delete=models.CASCADE)
    customerphone_created_at = models.DateTimeField(auto_now_add=True)
    customerphone_last_updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='customerphone_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='customerphone_modified', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'customerphones_new_03'
        ordering = ["-customer", '-phone']
        # verbose_name = 'customeremail'
        # verbose_name_plural = 'customeremails'

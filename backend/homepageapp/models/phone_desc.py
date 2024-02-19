from .base import models, InternalUser,FormattedPhoneNumberField


class PhoneDescModel(models.Model):
    phone_desc_id = models.IntegerField(primary_key=True)
    phone_desc = models.CharField(max_length=50, null=True)
    phone_order = models.IntegerField()
    phone_desc_default_type = models.CharField(max_length=5, null=True)
    phone_desc_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='phonedesc_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='phonedesc_modified', on_delete=models.SET_NULL, null=True, blank=True)
    phone_desc_last_updated_at = models.DateTimeField(
        auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    def __str__(self):
        return self.phone_desc
    
    class Meta:
        db_table = 'phonedescs_new_03'
        ordering = ["-phone_desc_id"]
        verbose_name = 'phonedesc'
        verbose_name_plural = 'phonedescs'

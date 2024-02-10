from .base import models, InternalUser, FormattedPhoneNumberField

class BrakesModel(models.Model):
    brake_id = models.AutoField(primary_key=True)
    brake_system_type = models.CharField(max_length=150, null=True, blank=True)
    brake_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='brake_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='brake_modified', on_delete=models.SET_NULL, null=True, blank=True)
    brake_last_updated_at = models.DateTimeField(
        auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    @property
    def get_brake_feature(self):
        fields = [str(self.brake_id), ": ", self.brake_system_type.strip()]

        brake_feature = "".join(
            [field for field in fields if field is not None])
        return brake_feature if brake_feature else "No available brake system found."

    class Meta:
        db_table = 'brakes_new_03'
        ordering = ["-brake_id"]
        verbose_name = 'brake'
        verbose_name_plural = 'brakes'

    def __str__(self):
        return self.get_brake_feature
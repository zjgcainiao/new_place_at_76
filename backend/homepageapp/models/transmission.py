from .base import models, InternalUser


class TransmissionsModel(models.Model):
    transmission_id = models.AutoField(primary_key=True)
    transmission_type = models.CharField(max_length=100, blank=True, null=True)
    transmission_manufacturer_code = models.CharField(
        max_length=100, blank=True, null=True)
    transmission_control_type = models.CharField(
        max_length=100, blank=True, null=True)
    transmission_is_electronic_controlled = models.BooleanField(default=False)
    transmission_number_of_speed = models.IntegerField(null=True, blank=True)
    transmission_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='transmission_created',
        on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='transmission_modified',
        on_delete=models.SET_NULL, null=True, blank=True)
    transmission_last_updated_at = models.DateTimeField(
        auto_now=True, null=True)

    @property
    def get_transmission_feature(self):
        fields = [str(self.transmission_id), ": ",
                  self.transmission_type.strip() if self.transmission_type else '',
                  "-", self.transmission_control_type,
                  "-",
                  self.transmission_manufacturer_code.strip() if self.transmission_manufacturer_code else '',
            '-',
            "electronic controlled" if str(self.transmission_is_electronic_controlled) else "not electronic controlled"]

        transmission_feature = "".join(
            [field for field in fields if field is not None])
        return transmission_feature if transmission_feature else "No available drive type."

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'transmissions_new_03'
        ordering = ["-transmission_id"]
        verbose_name = 'transmission'
        verbose_name_plural = 'transmissions'

    def __str__(self):
        return self.get_transmission_feature

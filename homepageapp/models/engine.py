from .base import models, InternalUser


class EnginesModel(models.Model):
    engine_id = models.AutoField(primary_key=True)
    engine_displacement_CID = models.DecimalField(
        max_digits=10, decimal_places=1, null=True)
    engine_displacement_liter = models.DecimalField(
        max_digits=10, decimal_places=1, null=True)
    engine_number_of_cylinder = models.IntegerField(null=True)
    engine_valve_per_cyclinder = models.IntegerField(null=True)
    engine_head_configuration_type = models.CharField(
        max_length=100, blank=True, null=True)
    engine_boost_type = models.CharField(max_length=100, blank=True, null=True)
    engine_ignition_system = models.CharField(
        max_length=100, blank=True, null=True)
    engine_vin_code = models.CharField(max_length=20, blank=True, null=True)
    engine_fuel_system = models.CharField(
        max_length=100, blank=True, null=True)
    engine_fuel_delivery_method_type = models.CharField(
        max_length=100, blank=True, null=True)
    engine_fuel_type = models.CharField(max_length=100, blank=True, null=True)
    engine_fuel_control_type = models.CharField(
        max_length=100, blank=True, null=True)
    engine_block_configuration = models.CharField(
        max_length=100, blank=True, null=True)
    engine_fuel_system_configuration = models.CharField(
        max_length=100, blank=True, null=True)
    engine_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='engine_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='engine_modified', on_delete=models.SET_NULL, null=True, blank=True)
    engine_last_updated_at = models.DateTimeField(auto_now=True, null=True)

    @property
    def get_engine_feature(self):
        fields = [str(self.engine_id), ": ",
                  str(self.engine_number_of_cylinder).strip(
        ) if self.engine_number_of_cylinder is not None else '',
            str(self.engine_valve_per_cyclinder).strip(
        ) if self.engine_valve_per_cyclinder is not None else '',
            "-", self.engine_vin_code if self.engine_vin_code is not None else '',
            "-", self.engine_fuel_type.strip() if self.engine_fuel_type is not None else '',
            "-", self.engine_head_configuration_type if self.engine_head_configuration_type is not None else '',
            "-", self.engine_boost_type.strip() if self.engine_boost_type is not None else '',
            "-", self.engine_fuel_type.strip() if self.engine_fuel_type is not None else '',
            "-", self.engine_fuel_system_configuration.strip() if self.engine_fuel_system_configuration is not None else '',
        ]
        engine_feature = "".join(
            [field for field in fields if field is not None])
        return engine_feature if engine_feature else "No available engine config cound."

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'engines_new_03'
        ordering = ["-engine_id"]
        verbose_name = 'engine'
        verbose_name_plural = 'engines'

    def __str__(self):
        return self.get_engine_feature
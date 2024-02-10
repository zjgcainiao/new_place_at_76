from .base import models, InternalUser

class DrivesModel(models.Model):
    drive_id = models.AutoField(primary_key=True)
    drive_type = models.CharField(max_length=150, null=True)
    drive_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='drive_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='drive_modified', on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def get_drive_type_feature(self):
        fields = [str(self.drive_id), ": ", self.drive_type.strip()]
        drive_type_feature = "".join(
            [field for field in fields if field is not None])
        return drive_type_feature if drive_type_feature else "No available drive type."

    def __str__(self):
        return self.get_drive_type_feature

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'drives_new_03'
        ordering = ["-drive_id"]
        verbose_name = 'drive'
        verbose_name_plural = 'drives'

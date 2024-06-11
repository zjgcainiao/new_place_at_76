from .base import models, InternalUser


class GVWsModel(models.Model):
    gvw_id = models.AutoField(primary_key=True)
    gvw_text = models.CharField(max_length=150, null=True)
    gvw_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='gvw_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='gvw_modified', on_delete=models.SET_NULL, null=True, blank=True)

    gvw_last_updated_at = models.DateTimeField(
        auto_now=True, null=True)

    @property
    def get_gvw_feature(self):
        fields = [str(self.gvw_id), ": ", self.gvw_text.strip()]

        gvw_feature = "".join(
            [field for field in fields if field is not None])
        return gvw_feature if gvw_feature else "No gross vehicle weight (GVW) found."

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'gvws_new_03'
        ordering = ["-gvw_id"]
        verbose_name = 'gvw'
        verbose_name_plural = 'gvws'

    def __str__(self):
        return self.get_gvw_feature

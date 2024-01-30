from .base import models, InternalUser

class BodyStylesModel(models.Model):
    body_style_id = models.AutoField(primary_key=True)
    body_style_name = models.CharField(max_length=150, null=True)
    body_style_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='body_style_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='body_style_modified', on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def get_body_style_feature(self):
        fields = [str(self.body_style_id), ": ", self.body_style_name.strip()]
        body_style_feature = "".join(
            [field for field in fields if field is not None])
        return body_style_feature if body_style_feature else "No available body style found."

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'bodystyles_new_03'
        ordering = ["-body_style_id"]
        verbose_name = 'bodystyle'
        verbose_name_plural = 'bodystyles'

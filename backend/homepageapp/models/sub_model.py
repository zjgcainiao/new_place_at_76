from .base import models, InternalUser
from .model import ModelsNewSQL02Model


class SubmodelsModel(models.Model):
    submodel_id = models.AutoField(primary_key=True)
    submodel_model = models.ForeignKey(
        ModelsNewSQL02Model, on_delete=models.CASCADE)
    submodel_name = models.CharField(max_length=150, null=True)
    submodel_DMV_id = models.IntegerField(null=True)
    submodel_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='submodel_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='submodel_modified', on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def get_sub_model_feature(self):
        fields = [str(self.submodel_id),
                  ": ", self.submodel_name.strip() if self.submodel_name is not None else ''
                  ]
        sub_model_feature = "".join(
            [field for field in fields if field is not None])
        return sub_model_feature if sub_model_feature else "No available sub model."

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'submodels_new_03'
        ordering = ["-submodel_id"]
        verbose_name = 'submodel'
        verbose_name_plural = 'submodels'

    def __str__(self):
        return self.get_sub_model_feature

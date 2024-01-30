from .base import models, InternalUser
from .make import MakesNewSQL02Model

class ModelsNewSQL02Model(models.Model):
    model_id = models.AutoField(primary_key=True)
    make = models.ForeignKey(MakesNewSQL02Model, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=30, null=True)
    model_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='model_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='model_modified', on_delete=models.SET_NULL, null=True, blank=True)
    make_last_updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'models_new_03'
        ordering = ["-model_id", 'make']
        verbose_name = 'model'
        verbose_name_plural = 'models'

    def __str__(self):
        return self.model_name.strip()

from .base import models, InternalUser

class MakesNewSQL02Model(models.Model):
    make_id = models.AutoField(primary_key=True)
    make_name = models.CharField(max_length=30, null=True)
    make_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='make_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='make_modified', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'makes_new_03'
        ordering = ["-make_id"]
        verbose_name = 'make'
        verbose_name_plural = 'makes'

    def __str__(self):
        return f'{self.make_name.strip()}'
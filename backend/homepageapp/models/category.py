from .base import models, InternalUser

class CategoryModel(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_description = models.CharField(
        max_length=200, blank=True, null=True)
    category_display = models.IntegerField(blank=True, null=True)
    category_created_at = models.DateTimeField(auto_now_add=True)
    # tracking fields
    created_by = models.ForeignKey(
        InternalUser, related_name='category_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='category_modified', on_delete=models.SET_NULL, null=True, blank=True)
    category_last_updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return f"{self.category_id}-{self.category_description}"
    

    class Meta:
        db_table = 'categories_new_03'
        ordering = ['-category_id']

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)
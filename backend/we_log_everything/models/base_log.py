from .base import models, InternalUser, CustomerUser


class BaseLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    # The specific choices will be defined in the subclasses
    action = models.CharField(max_length=254)
    description = models.TextField()
    description_in_json = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # Makes this model abstract
        ordering = ['-created_at']

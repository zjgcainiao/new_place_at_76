from .base import models, InternalUser


class Operator(models.Model):
    id = models.AutoField(primary_key=True)
    internal_user = models.OneToOneField(
        InternalUser, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'operators'
        verbose_name = 'Operator'
        verbose_name_plural = 'Operators'
        ordering = ["-id",]
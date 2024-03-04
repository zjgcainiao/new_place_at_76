from .base import models
from internal_users.models import InternalUser
# store the list of available ai models provided by OpenAI


class OpenAIModel(models.Model):
    id = models.AutoField(primary_key=True)
    # the model_id prvovided by OpenAI
    model_id = models.CharField(
        max_length=100, unique=True, verbose_name='model id')
    model_created = models.DateTimeField()
    model_type = models.CharField(max_length=100, null=True, blank=True)
    model_owned_by = models.CharField(max_length=100, null=True, blank=True)
    model_comments = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(InternalUser, on_delete=models.DO_NOTHING,
                                   null=True, blank=True,
                                   related_name='openai_models_created_by',
                                   )
    updated_by = models.ForeignKey(InternalUser, on_delete=models.DO_NOTHING,
                                   null=True, blank=True,
                                   related_name='openai_models_updated_by')

    def __str__(self):
        return self.model_id

    class Meta:
        db_table = "openai_models"
        ordering = ["id", "-model_created"]

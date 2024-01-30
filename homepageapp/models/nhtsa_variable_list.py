from .base import models, InternalUser

# created 2023-10-18. store the variable_name info and its group name. updated by management script "populate_nhtsa_variable_list".

class NhtsaVariableList(models.Model):
    id = models.AutoField(primary_key=True)
    variable_id = models.IntegerField(unique=True, default=None)
    variable_name = models.CharField(max_length=200, null=True, blank=True)
    variable_group_name = models.CharField(
        max_length=200, null=True, blank=True)
    variable_description_html = models.CharField(
        max_length=4000, null=True, blank=True)
    variable_data_type = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'nhtsa_variable_list'
        ordering = ["-id", 'variable_id']



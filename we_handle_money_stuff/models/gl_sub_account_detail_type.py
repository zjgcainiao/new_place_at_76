from .base import models,InternalUser

class GLSubAccountDetailType(models.Model):
    id= models.AutoField(primary_key=True)
    name = models.CharField(max_length=100) # name of the sub account detail type, e.g. "Cash", "Accounts Receivable", Employee Cash Advance"
    description = models.TextField(null=True, blank=True) # optional, explain the type of sub account
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(InternalUser, related_name='sub_account_detail_type_created_by', on_delete=models.DO_NOTHING, null=True, blank=True)
    updated_by = models.ForeignKey(InternalUser, related_name='sub_account_detail_type_updated_by', on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        db_table = 'gl_sub_account_detail_type'
        verbose_name = 'GL Sub Account Detail Type'
        verbose_name_plural = 'GL Sub Account Detail Types'
        ordering = ['id']
        unique_together = ('name', 'is_active')
        permissions = [
            ('view_gl_sub_account_detail_type', 'Can view GL Sub Account Detail Type'),
            ('create_gl_sub_account_detail_type', 'Can create GL Sub Account Detail Type'),
            ('edit_gl_sub_account_detail_type', 'Can edit GL Sub Account Detail Type'),
            ('delete_gl_sub_account_detail_type', 'Can delete GL Sub Account Detail Type'),
        ]
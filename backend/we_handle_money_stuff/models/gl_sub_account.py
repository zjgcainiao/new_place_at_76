from .base import models,InternalUser
from .gl_account import GLAccount
from .gl_sub_account_type import GLSubAccountType
from .gl_sub_account_detail_type import GLSubAccountDetailType

class GLSubAccount(models.Model):
    id = models.AutoField(primary_key=True)
    sub_account_number = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    parent_account = models.ForeignKey(GLAccount, on_delete=models.CASCADE,null=True, blank=True, related_name='sub_accounts')
    sub_account_type = models.ForeignKey(GLSubAccountType, on_delete=models.DO_NOTHING, null=True, blank=True)
    sub_account_detail_type = models.ForeignKey(GLSubAccountDetailType, on_delete=models.DO_NOTHING, null=True,blank=True)
    is_active = models.BooleanField(default=True) # soft delete flag
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(InternalUser, related_name='gl_sub_account_created_by', on_delete=models.DO_NOTHING, null=True, blank=True)
    updated_by = models.ForeignKey(InternalUser, related_name='gl_sub_account_updated_by', on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return f'{self.sub_account_number}_{self.name}'
    class Meta:
        db_table = 'gl_sub_account'
        verbose_name = 'GL Sub Account'
        verbose_name_plural = 'GL Sub Accounts'
        ordering = ['id']
        unique_together = ('sub_account_number', 'is_active')
        permissions = [
            ('view_gl_sub_account', 'Can view GL Sub Account'),
            ('create_gl_sub_account', 'Can create GL Sub Account'),
            ('edit_gl_sub_account', 'Can edit GL Sub Account'),
            ('delete_gl_sub_account', 'Can delete GL Sub Account'),
        ]


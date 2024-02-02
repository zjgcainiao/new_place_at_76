from .base import models
from .gl_account import GLAccount
from .gl_sub_account_type import GLSubAccountType
from .gl_sub_account_detail_type import GLSubAccountDetailType

class GLSubAccount(models.Model):
    name = models.CharField(max_length=255)
    sub_account_number = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    parent_account = models.ForeignKey(GLAccount, on_delete=models.CASCADE)
    sub_account_type = models.ForeignKey(GLSubAccountType, on_delete=models.SET_NULL, null=True, blank=True)
    sub_account_detail_type = models.ForeignKey(GLSubAccountDetailType, on_delete=models.SET_NULL, null=True,blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('InternalUser', related_name='gl_sub_account_created_by', on_delete=models.DO_NOTHING, null=True, blank=True)
    updated_by = models.ForeignKey('InternalUser', related_name='gl_sub_account_updated_by', on_delete=models.DO_NOTHING, null=True, blank=True)

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


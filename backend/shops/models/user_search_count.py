from .base import models, settings, InternalUser, CustomerUser


class UserSearchCount(models.Model):
    customer_user = models.OneToOneField(CustomerUser, on_delete=models.DO_NOTHING,null=True, blank=True)
    search_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(InternalUser, on_delete=models.DO_NOTHING, related_name='user_search_count_created_by')
    updated_by = models.ForeignKey(InternalUser, on_delete=models.DO_NOTHING, related_name='user_search_count_updated_by')

    def __str__(self):
        return f"{self.customer_user} - {self.search_count}"

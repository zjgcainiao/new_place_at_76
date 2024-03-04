
from django.db import models
from customer_users.models import CustomerUser
from internal_users.models import InternalUser

# build to track the number of searches by anonymous users in React Native app


class AnonymousUserSearchCount(models.Model):
    customer_user = models.OneToOneField(
        CustomerUser, on_delete=models.DO_NOTHING, null=True, blank=True)
    search_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        InternalUser, on_delete=models.DO_NOTHING, related_name='user_search_count_created_by')
    updated_by = models.ForeignKey(
        InternalUser, on_delete=models.DO_NOTHING, related_name='user_search_count_updated_by')

    def __str__(self):
        return f"{self.customer_user} - {self.search_count}"

    class Meta:
        db_table = "anonymous_user_search_count"
        verbose_name_plural = "Anonymous User Search Counts"
        verbose_name = "Anonymous User Search Count"
        ordering = ['-created_at']

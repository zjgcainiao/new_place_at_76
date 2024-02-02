from .base import models, settings, InternalUser, CustomerUser


class UserSearchCount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    search_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.search_count}"

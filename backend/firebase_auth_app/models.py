from django.db import models
from django.contrib.auth.models import AbstractUser
# import uuid

# Create your models here.
class FirebaseUser(models.Model):
    # uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firebase_user_id = models.BigIntegerField(primary_key=True)
    uid = models.CharField(max_length=100, null=True)
    display_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    email_is_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, null=True)
    photo_url = models.URLField( null=True, blank=True)
    latest_token = models.CharField(max_length=1000, null=True)
    latest_token_exp = models.DateTimeField(null=True)

    firebase_user_disabled  = models.BooleanField(default=False)
    firebase_user_providers = models.CharField(max_length=200, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # if not self.pk:
            # Only set the talent_created_by_user_id if this is a new instance
            # self.talent_created_by_user_id = request.user.id
        # super(TalentsModel, self).save(*args, **kwargs)

        # firebase_user_id, manually incremental.
        if not self.firebase_user_id:
            last_firebase_user = FirebaseUser.objects.order_by('-firebase_user_id').first()
            if last_firebase_user:
                self.firebase_user_id = last_firebase_user.firebase_user_id + 1
            else:
                self.firebase_user_id = 1
        else:
            self.firebase_user_id = 1

        super().save(*args, **kwargs)

    class Meta:
        db_table = 'firebase_users'
        ordering =['-firebase_user_id']
        verbose_name = 'firebaseuser'
        verbose_name_plural = 'firebaseusers'
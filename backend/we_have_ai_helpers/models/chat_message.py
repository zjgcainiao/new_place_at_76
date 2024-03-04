from django.db import models
from django.contrib.auth.models import User  # If you have user authentication
from customer_users.models import CustomerUser
from internal_users.models import InternalUser


class ChatMessage(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer_user = models.ForeignKey(
        CustomerUser, on_delete=models.DO_NOTHING, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    message_role = models.CharField(max_length=100, null=True, blank=True)
    question = models.TextField(null=True, blank=True)
    answer = models.TextField(null=True, blank=True)
    chat_history = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(InternalUser, on_delete=models.DO_NOTHING,
                                   null=True, blank=True,
                                   related_name='chat_messages_created_by',
                                   )
    updated_by = models.ForeignKey(InternalUser, on_delete=models.DO_NOTHING,
                                   null=True, blank=True,
                                   related_name='chat_messages_updated_by')

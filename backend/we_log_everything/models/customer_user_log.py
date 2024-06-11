from .base_log import BaseLog
from .base import models, InternalUser, CustomerUser

ACTION_CHOICES = [
    ('customer_user_created', 'Customer User Created'),
    ('customer_user_updated', 'Customer User Updated'),
    ('customer_user_deleted', 'Customer User Deleted'),
    ('customer_user_logged_in', 'Customer User Logged In'),
    ('customer_user_logged_out', 'Customer User Logged Out'),
    ('customer_user_suspicious_activity_raised',
     'Customer User Suspicious Activity Raised'),
    ('customer_user_suspicious_activity_resolved',
     'Customer User Suspicious Activity Resolved'),
    ('customer_user_password_reset', 'Customer User Password Reset'),
    ('customer_user_password_changed', 'Customer User Password Changed'),
    ('customer_user_profile_updated', 'Customer User Profile Updated'),
    ('customer_user_subscribed', 'Customer User Subscribed'),
    ('customer_user_unsubscribed', 'Customer User Unsubscribed'),
    ('customer_user_one_time_purchase', 'Customer User One Time Purchase'),
    ('customer_user_request_refund', 'Customer User Request Refund'),
    ('customer_user_refund_processed', 'Customer User Refund Processed'),
    ('customer_user_other', 'Customer User Other'),
]


class CustomerUserLog(BaseLog):
    id = models.BigAutoField(primary_key=True)
    action = models.CharField(max_length=255, choices=ACTION_CHOICES)
    customer_user = models.ForeignKey(CustomerUser,
                                      on_delete=models.DO_NOTHING,
                                      null=True, blank=True,
                                      related_name='customer_user_logs')

    def __str__(self):

        return f"{self.customer_user} performed {self.action} at {self.created_at: %Y-%m-%d %H:%M}."

    class Meta:
        db_table = 'customer_user_logs'
        verbose_name = 'Customer User Log'
        verbose_name_plural = 'Customer User Logs'

from .base_log import BaseLog
from .base import models, InternalUser
from homepageapp.models import RepairOrdersNewSQL02Model as RepairOrder

ACTION_CHOICES = [
    ('repair_order_created', 'Repair Order Created'),
    ('repair_order_deleted', 'Repair Order Deleted'),
    ('repair_order_payment_success', 'Repair Order has been Paid Successfully'),
    ('repair_order_deactivated', 'Repair Order Deactivated/Soft Deleted'),
    ('repair_order_vehicle_updated', 'Vehicle Info Updated on Repair Order'),
    ('repair_order_customer_updated', 'Customer Info Updated on Repair Order'),

    ('repair_order_status_changed', 'Repair Order Status Changed'),
    ('repair_order_completed', 'Repair Order has been completed.'),
    ('repair_order_amount_changed', 'Repair Order Amount Due Changed'),
    ('repair_order_action_required', 'Repair Order Action Required'),
    ('repair_order_critical_error', 'Repair Order has logged an critical error'),
    ('repair_order_refund_processed', 'Repair Order Refund Processed'),
    ('repair_order_other', 'Repair Order Other'),
]


class RepairOrderLog(BaseLog):
    id = models.BigAutoField(primary_key=True)
    action = models.CharField(max_length=200, choices=ACTION_CHOICES)

    internal_user = models.ForeignKey(InternalUser,
                                      on_delete=models.DO_NOTHING,
                                      null=True, blank=True,
                                      related_name='repair_order_logs_by_internal_user')
    repair_order = models.ForeignKey(RepairOrder,
                                     on_delete=models.DO_NOTHING,
                                     null=True, blank=True,
                                     related_name='repair_order_logs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        return f"{self.repair_order} performed {self.action} at {self.created_at: %Y-%m-%d %H:%M}."

    class Meta:
        db_table = 'repair_order_logs'
        verbose_name = 'Repair Order Log'
        verbose_name_plural = 'Repair Order Logs'
        ordering = ['-created_at']

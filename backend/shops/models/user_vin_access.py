
from .base import models

from internal_users.models import InternalUser
from customer_users.models import CustomerUser
# from homepageapp.models import Vin
from .vin import Vin

# This model is used to store the access of a user to a VIN. Vin Model stores the most comprehensive information about a vehicle,
# it collect information from multiple sources, including NHTSA, RepairOrder, and other sources. Each source has its own model.
# by definiting foreign key to Vin model, this model can be used to store the access information of a user to a vehicle.


class UserVINAccess(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField()
    customer_user = models.ForeignKey(CustomerUser,
                                      on_delete=models.DO_NOTHING, null=True,
                                      blank=True)
    internal_user = models.ForeignKey(InternalUser,
                                      on_delete=models.DO_NOTHING, null=True,
                                      blank=True)
    vin = models.ForeignKey(Vin, on_delete=models.DO_NOTHING,
                            related_name='user_accesses')
    is_paid = models.BooleanField(default=False)
    # Optional, if paid is True #stripe
    payment_intent_id = models.CharField(max_length=100, null=True, blank=True)
    paid_record_json = models.JSONField(
        null=True, blank=True)  # Optional, if paid is True
    # Optional, if access is time-limited
    access_expires = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_vin_access'
        ordering = ["-id", 'email', 'vin']
        # Ensure each user-VIN pair is unique
        unique_together = ('email', 'vin')

    def __str__(self):
        return f"{self.email} - {self.vin} - {'Paid' if self.is_paid else 'Not Paid'}"

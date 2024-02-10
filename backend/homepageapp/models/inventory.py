from .base import models, InternalUser

from .part import PartsModel


class Inventories(models.Model):

    inventory_id = models.AutoField(primary_key=True)
    inventory_part = models.ForeignKey(
        PartsModel, on_delete=models.CASCADE, related_name='inventory_part')
    inventory_on_hand = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    inventory_on_order = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    inventory_location = models.CharField(max_length=80, null=True, blank=True)
    inventory_last_sold_at = models.DateTimeField(null=True, blank=True)
    inventory_available_quantity = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    inventory_committed_quantity = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)
    ivnentory_condition_id = models.IntegerField(null=True, blank=True)
    inventory_superceded_by = models.ForeignKey(
        PartsModel, on_delete=models.CASCADE, related_name='inventory_part_superceded_by', null=True, blank=True)
    inventory_restock_quantity = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True)
    inventory_order_point = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True)
    inventory_core_quantity = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True)
    inventory_does_pay_comission = models.BooleanField(default=False)
    inventory_total_cost_amount = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True)
    inventory_last_cost_amount = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True)
    inventory_prior_to_last_cost_amount = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True)
    updated_at = models.DateTimeField(
        auto_now=True, null=True)
    updated_by = models.ForeignKey(
        InternalUser, related_name='inventory_updated_by', on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(
        auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='inventory_created_by', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'inventories_new_03'
        ordering = ["-inventory_id", '-created_at']
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventories'

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.updated_by
        super().save(*args, **kwargs)
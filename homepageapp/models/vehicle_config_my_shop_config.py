from .base import models, InternalUser
from .my_shop_vehicle_config import MyShopVehicleConfigsModel

class VehicleConfigMyShopConfigsModel(models.Model):
    vehicle_config_id = models.AutoField(primary_key=True)
    myshop_vehicle_config = models.ForeignKey(MyShopVehicleConfigsModel,
                                              on_delete=models.SET_NULL, null=True, related_name='vehicleconfigmyshopconfigs')
    vehicle_config_myshop_config_created_at = models.DateTimeField(
        auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='vehicle_config_myshop_config_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='vehicle_config_myshop_config_modified', on_delete=models.SET_NULL, null=True, blank=True)

    # Methods
    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super(MyShopVehicleConfigsModel, self).save(*args, **kwargs)

    class Meta:
        db_table = 'vehicleconfigmyshopconfigs_new_03'
        ordering = ["-vehicle_config_id"]
        verbose_name = 'vehicleconfigmyshopconfig'
        verbose_name_plural = 'vehicleconfigmyshopconfigs'
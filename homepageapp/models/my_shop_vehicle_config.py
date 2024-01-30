from .base import models, InternalUser
from .make import MakesNewSQL02Model
from .model import ModelsNewSQL02Model
from .sub_model import SubmodelsModel
from .body_style import BodyStylesModel
from .engine import EnginesModel
from .brake import BrakesModel
from .transmission import TransmissionsModel    
from .gvw import GVWsModel
from .drive import DrivesModel

class MyShopVehicleConfigsModel(models.Model):
    myshop_vehicle_config_id = models.AutoField(primary_key=True)
    myshop_year_id = models.IntegerField(null=True)
    myshop_make = models.ForeignKey(
        MakesNewSQL02Model, on_delete=models.SET_NULL, null=True, related_name='myshop_makes')
    myshop_model = models.ForeignKey(
        ModelsNewSQL02Model, on_delete=models.SET_NULL, null=True, related_name='myshop_models')
    myshop_submodel = models.ForeignKey(
        SubmodelsModel, on_delete=models.SET_NULL, null=True, related_name='myshop_submodels')
    myshop_bodystyle = models.ForeignKey(
        BodyStylesModel, on_delete=models.SET_NULL, null=True, related_name='myshop_bodystyles')
    myshop_engine = models.ForeignKey(
        EnginesModel, on_delete=models.SET_NULL, null=True, related_name='myshop_engines')
    myshop_brake = models.ForeignKey(
        BrakesModel, on_delete=models.SET_NULL, null=True, related_name='myshop_brakes')
    myshop_transmission = models.ForeignKey(
        TransmissionsModel, on_delete=models.SET_NULL, null=True, related_name='myshop_transmissions')
    myshop_GVW = models.ForeignKey(
        GVWsModel, on_delete=models.SET_NULL, null=True, related_name='myshop_gvws')
    myshop_drive = models.ForeignKey(
        DrivesModel, on_delete=models.SET_NULL, null=True, name='myshop_drives')
    myshop_vehicle_config_created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='myshop_vehicle_config_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='myshop_vehicle_config_modified', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'myshopvehicleconfigs_new_03'
        ordering = ["-myshop_vehicle_config_id"]
        verbose_name = 'myshop vehicle configuration'
        verbose_name_plural = 'myshop vehicle configurations'

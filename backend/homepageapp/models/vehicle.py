from .base import models, InternalUser
from .customer import CustomersNewSQL02Model
from . make import MakesNewSQL02Model  
from .sub_model import SubmodelsModel
from .body_style import BodyStylesModel
from .engine import EnginesModel 
from .transmission import TransmissionsModel
from .brake import BrakesModel
from .gvw import GVWsModel
from .drive import DrivesModel
from .phone import PhonesNewSQL02Model  

class VehiclesNewSQL02Model(models.Model):
    # vehicle_new_uid_v01 = models.CharField(editable=False, auto_created=True, primary_key=True, max_length=36)  # default = uuid.uuid4
    vehicle_id = models.AutoField(primary_key=True)
    vehicle_cust = models.ForeignKey(
        CustomersNewSQL02Model, on_delete=models.SET_NULL, null=True, related_name='vehicle_customers', blank=True)
    vehicle_year = models.CharField(max_length=20, null=True, blank=True)
    vehicle_make = models.ForeignKey(
        MakesNewSQL02Model, on_delete=models.SET_NULL, null=True, related_name='vehicle_makes', blank=True)
    vehicle_sub_model = models.ForeignKey(
        SubmodelsModel, on_delete=models.SET_NULL, null=True, related_name='vehicle_submodels', blank=True)
    vehicle_body_style = models.ForeignKey(
        BodyStylesModel, on_delete=models.SET_NULL, null=True, related_name='vehicle_bodystyles', blank=True)
    vehicle_engine = models.ForeignKey(
        EnginesModel, on_delete=models.SET_NULL, null=True, related_name='vehicle_engines', blank=True)
    vehicle_transmission = models.ForeignKey(
        TransmissionsModel, on_delete=models.SET_NULL, null=True, related_name='vehicle_transmissions', blank=True)
    vehicle_brake = models.ForeignKey(
        BrakesModel, on_delete=models.SET_NULL, null=True, related_name='vehicle_brakes', blank=True)
    vehicle_drive_type = models.ForeignKey(
        DrivesModel, on_delete=models.SET_NULL, null=True, related_name='vehicle_drives', blank=True)
    vehicle_gvw = models.ForeignKey(
        GVWsModel, on_delete=models.SET_NULL, null=True, related_name='vehicle_gvws', blank=True)
    vehicle_odometer_1 = models.BigIntegerField(null=True, blank=True)
    vehicle_odometer_2 = models.BigIntegerField(null=True, blank=True)
    VIN_number = models.CharField(max_length=50, null=True, blank=True)
    vehicle_inspection_datetime = models.DateTimeField(null=True, blank=True)
    vehicle_last_in_date = models.DateTimeField(null=True, blank=True)
    vehicle_license_plate_nbr = models.CharField(
        max_length=20, null=True, blank=True)
    vehicle_license_state = models.CharField(
        max_length=20, null=True, blank=True)
    vehicle_part_level = models.CharField(max_length=20, null=True, blank=True)
    vehicle_labor_level = models.CharField(
        max_length=20, null=True, blank=True)
    vehicle_used_level = models.CharField(max_length=20, null=True, blank=True)
    vehicle_memo_01 = models.CharField(max_length=4000, null=True, blank=True)
    vehicle_memo_does_print_on_order = models.BooleanField(default=False)
    vehicle_is_included_in_crm_compaign = models.BooleanField(default=True)
    vehicle_color = models.CharField(max_length=20, null=True, blank=True)

    vehicle_record_is_active = models.BooleanField(default=True)
    vehicle_class_id = models.CharField(max_length=20, null=True, blank=True)
    vehicle_engine_hour_in = models.DecimalField(
        max_digits=7, decimal_places=1, blank=True)
    vehicle_engine_hour_out = models.DecimalField(
        max_digits=7, decimal_places=1, blank=True)
    vehicle_active_recall_counts = models.IntegerField(null=True, blank=True)
    vehicle_recall_last_checked_datetime = models.DateTimeField(
        null=True, blank=True)
    vehicle_phone = models.ForeignKey(
        PhonesNewSQL02Model, on_delete=models.SET_NULL, null=True, blank=True, related_name='vehicle_phones',)
    vehicle_contact_phone_main_new_uid = models.CharField(
        max_length=36, null=True, blank=True)

    vehicle_authorized_customers = models.ManyToManyField(
        'CustomersNewSQL02Model', related_name='authorized_vehicles', blank=True)

    vehicle_created_at = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(
        InternalUser, related_name='vehicle_created', on_delete=models.SET_NULL, null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='vehicle_modified', on_delete=models.SET_NULL, null=True, blank=True)
    vehicle_last_updated_at = models.DateTimeField(
        auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    def __str__(self):
        # Handling the case where vehicle_make or vehicle_make.vehicle_makes is None
        # Handling the case where vehicle_make is None
        make_name = self.vehicle_make.make_name if self.vehicle_make else 'Unknown Make'
        return f"VehicleID_{self.vehicle_id}_{self.vehicle_year}_{make_name}"
    class Meta:
        db_table = 'vehicles_new_03'
        ordering = ["-vehicle_id"]
        verbose_name = 'vehicle'
        verbose_name_plural = 'vehicles'

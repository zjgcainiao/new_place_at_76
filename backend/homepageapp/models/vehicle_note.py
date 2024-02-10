from .base import models, InternalUser
from .vehicle import VehiclesNewSQL02Model
from core_operations.constants import VEHICLE_NOTE_TYPES

class VehicleNotesModel(models.Model):
    vehicle_note_id = models.AutoField(primary_key=True)
    vehicle_note_type = models.CharField(max_length=100, choices=VEHICLE_NOTE_TYPES,null=True, blank=True)
    vehicle = models.ForeignKey(
        VehiclesNewSQL02Model, on_delete=models.SET_NULL, null=True, blank=True, related_name='vehiclenotes_vehicle')
    vehicle_note_text = models.CharField(max_length=400, null=True, blank=True)
    vehicle_note_is_active = models.BooleanField(default=True)
    vehicle_note_last_updated_at = models.DateTimeField(
        auto_now=True, null=True)
    vehicle_note_created_at = models.DateTimeField(
        auto_now_add=True, null=True)

    created_by = models.ForeignKey(
        InternalUser, related_name='vehicle_note_created', 
        on_delete=models.SET_NULL, 
        null=True, blank=True)
    modified_by = models.ForeignKey(
        InternalUser, related_name='vehicle_note_modified', 
        on_delete=models.SET_NULL, 
        null=True, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.modified_by
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'vehiclenotes_new_03'
        ordering = ['-vehicle_note_id']
        verbose_name = 'vehicle_note'
        verbose_name_plural = 'vehicle_notes'
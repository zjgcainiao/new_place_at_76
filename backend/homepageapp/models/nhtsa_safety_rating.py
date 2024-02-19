import decimal
from tabnanny import verbose
from .base import models, InternalUser
from .nhtsa_vehicle_id import NhtsaVehicleId
# https://api.nhtsa.gov/SafetyRatings/VehicleId/8476

class NhtsaSafetyRating(models.Model):
    id = models.BigAutoField(primary_key=True)
    vin = models.CharField(max_length=30,null=True, blank=True)
    vehicle_picture_url = models.URLField(max_length=1500, null=True, blank=True)

    overall_rating = models.CharField(max_length=100, null=True, blank=True)
    overall_front_crash_rating = models.CharField(
        max_length=30, null=True, blank=True)
    front_crash_drivers_side_rating = models.CharField(
        max_length=30, null=True, blank=True)
    front_crash_passengers_side_rating = models.CharField(
        max_length=30, null=True, blank=True)
    front_crash_picture_url = models.URLField(max_length=1500, null=True, blank=True)

    front_crash_video_url = models.URLField(max_length=1500, null=True, blank=True)

    overall_side_crash_rating = models.CharField(
        max_length=30, null=True, blank=True)
    
    side_crash_drivers_side_rating = models.CharField(
        max_length=30, null=True, blank=True)
    side_crash_passengers_side_rating = models.CharField(
        max_length=30, null=True, blank=True)
    side_crash_picture_url = models.URLField(max_length=1500, null=True, blank=True)

    side_crash_video_url = models.URLField(max_length=1500, null=True, blank=True)
    
    combined_side_barrier_and_pole_rating_front= models.CharField(
        max_length=30, null=True, blank=True)
    combined_side_barrier_and_pole_rating_rear= models.CharField(
        max_length=30, null=True, blank=True)
    combined_side_barrier_rating_overall= models.CharField(
        max_length=30, null=True, blank=True)

    side_pole_crash_rating = models.CharField(
        max_length=30, null=True, blank=True)
    side_pole_picture_url = models.URLField(max_length=1500, null=True, blank=True)
    side_pole_video_url = models.URLField(max_length=1500, null=True, blank=True)

    dynamic_tip_result = models.CharField(
        max_length=30, null=True, blank=True)
    
    rollover_rating = models.CharField(
        max_length=30, null=True, blank=True)

    rollover_rating_2 = models.CharField(
        max_length=30, null=True, blank=True)
    rollover_possiblity = models.DecimalField(
                    decimal_places=2, max_digits=5, null=True, blank=True)
    rollover_possiblity_2 = models.DecimalField(decimal_places=2, max_digits=5, null=True, blank=True)

    
    nhtsa_electronic_stability_control=models.CharField(
        max_length=60, null=True, blank=True)
    nhtsa_forward_collision_warning=models.CharField(
        max_length=60, null=True, blank=True)
    nhtsa_lane_departure_warning=models.CharField(
        max_length=60, null=True, blank=True)
    complaints_count=models.IntegerField(null=True, blank=True)
    recalls_count=models.IntegerField(null=True, blank=True)
    investigation_count=models.IntegerField(null=True, blank=True)
    model_year=models.IntegerField(null=True, blank=True)
    make=models.CharField(max_length=100, null=True, blank=True)
    model=models.CharField(max_length=50, null=True, blank=True)
    vehicle_description=models.CharField(max_length=500, null=True, blank=True)
    vehicle_id = models.ForeignKey(NhtsaVehicleId, on_delete=models.DO_NOTHING, null=True, related_name='vehicle_id_nhtsa_safety_ratings')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='Updated at')
    created_by = models.ForeignKey(InternalUser, on_delete=models.DO_NOTHING,
                                   null=True, related_name='nhtsa_safety_rating_created_by')

    updated_by = models.ForeignKey(InternalUser, on_delete=models.DO_NOTHING,
                                   null=True, related_name='nhtsa_safety_rating_updated_by')

    def __str__(self):
        return f'{self.vin}-{self.overall_rating}'

    class Meta:
        db_table = 'nhtsa_safety_ratings'
        ordering = ["-id", 'vin']
        indexes = [
            models.Index(fields=['vin']),
        ]
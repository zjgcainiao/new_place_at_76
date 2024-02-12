
from .base import models, InternalUser, gettext_lazy as _
from .appointment_request import AppointmentRequest

class AppointmentImages(models.Model):
    image_id = models.BigAutoField(primary_key=True)
    appointment = models.ForeignKey(AppointmentRequest, on_delete=models.SET_NULL,
                                    null=True, related_name='appointment_appointmentimages')
    appointment_image = models.FileField(
        upload_to='appointment_images')  # the bucket's subfolder

    image_is_active = models.BooleanField(default=True)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        InternalUser, on_delete=models.SET_NULL, null=True, related_name='image_created_by')  # when null, it means its created by customer user

    class Meta:

        db_table = 'appointment_images'
        ordering = ['-image_id']
        verbose_name = 'appointment_image'
        verbose_name_plural = 'appointment_images'

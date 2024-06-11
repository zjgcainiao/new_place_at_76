
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
        # when null, it means its created by customer user
        InternalUser, on_delete=models.SET_NULL, null=True, related_name='image_created_by')

    class Meta:

        db_table = 'appointment_images'
        ordering = ['-image_id']
        verbose_name = 'Appointment Image'
        verbose_name_plural = 'Appointment Images'

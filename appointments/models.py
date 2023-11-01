from django.utils.translation import gettext_lazy as _
from django.db import models
import uuid
from internal_users.models import InternalUser
from customer_users.models import CustomerUser
from homepageapp.models import RepairOrdersNewSQL02Model as RepairOrder
from django.utils import timezone
from core_operations.models import FormattedPhoneNumberField

APPT_STATUS_NOT_SUBMITTED = 0
APPT_STATUS_PENDING = 1
APPT_STATUS_CONFIRMED = 2
APPT_STATUS_REJECTED = 3
APPT_STATUS_RESCHEDULED = 4
APPT_STATUS_PORGRESSING = 5
APPT_STATUS_COMPLETED = 10
APPT_STATUS_CANCELLED = -20


class AppointmentRequest(models.Model):
    STATUS_CHOICES = (
        (APPT_STATUS_NOT_SUBMITTED, _('00_Not_Submitted')),
        (APPT_STATUS_PENDING, _('01_Pending')),
        (APPT_STATUS_CONFIRMED, _('02_Confirmed')),
        (APPT_STATUS_REJECTED, _('03_Rejected')),
        (APPT_STATUS_RESCHEDULED, _('04_Rescheduled')),
        (APPT_STATUS_PORGRESSING, _('05_Progressing (tracking status via repair order)')),
        (APPT_STATUS_COMPLETED, _('10_Completed')),
        (APPT_STATUS_CANCELLED, _('-20_Cancelled')),
    )
    REASON_CHOICES = (
        (0, '00-not selected.'),
        (1, '01-oil change and maintenance.'),
        (2, '02-a/c diagnosis, compressors etc.'),
        (3, '03-brakes, transmission'),
        (4, '04-service lights, engine related'),
        (5, '05-just inqurires, others'),
    )
    appointment_id = models.BigAutoField(primary_key=True)
    # appointment_date = models.DateField()
    appointment_requested_datetime = models.DateTimeField(
        null=True, blank=True, verbose_name='Requested Apptmnt Time')
    appointment_confirmed_datetime = models.DateTimeField(
        null=True, blank=True, verbose_name='Confirmed Apptmnt Time')
    appointment_reason_for_visit = models.PositiveSmallIntegerField(
        choices=REASON_CHOICES, default=0, verbose_name='Reason for visit?')
    appointment_customer_user = models.ForeignKey(
        CustomerUser, on_delete=models.SET_NULL, null=True, verbose_name='your linked user account')
    appointment_first_name = models.CharField(
        max_length=50, null=True, blank=True)
    appointment_last_name = models.CharField(
        max_length=50, null=True, blank=True)
    appointment_phone_number = FormattedPhoneNumberField(
        help_text='we will send appointment reminders to this number.')
    appointment_phone_number_digits_only = models.CharField(
        max_length=20, null=True)
    # recording either customer_user or internal_user
    appointment_user_type = models.CharField(
        max_length=50, blank=True, null=True)
    appointment_email = models.EmailField(null=True)
    appointment_vehicle_year = models.CharField(
        max_length=4, null=True, blank=True)
    appointment_vehicle_make = models.CharField(
        max_length=100, null=True, blank=True)
    appointment_vehicle_model = models.CharField(
        max_length=100, null=True, blank=True)
    appointment_vehicle_license_plate = models.CharField(
        max_length=20, null=True, blank=True)
    appointment_vehicle_license_state = models.CharField(
        max_length=2, null=True, blank=True)
    appointment_vehilce_vin_number = models.CharField(
        max_length=30, null=True, blank=True)
    appointment_vehicle_detail = models.TextField()
    appointment_vehicle_detail_in_json = models.CharField(
        max_length=4000, null=True)  # {'year': 2003, 'model': VW, ...}
    appointment_concern_description = models.TextField(blank=True)

    # check the status of the appointment
    appointment_status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default=APPT_STATUS_NOT_SUBMITTED, verbose_name='Appointment Status')
    appointment_status_comments = models.CharField(
        max_length=4000, null=True, blank=True)
    appointment_is_active = models.BooleanField(default=True)
    appointment_preferred_contact_method = models.CharField(
        max_length=100, blank=True, null=True)
    appointment_repair_order = models.ForeignKey(
        RepairOrder, on_delete=models.SET_NULL, null=True, related_name='appointment_repair_order')
    appointment_is_converted_to_ro = models.BooleanField(default=False)
    appointment_confirmation_id = models.UUIDField(
        default=uuid.uuid4, editable=False,  verbose_name='your appointment confirmation id')  # unique=True,
    # appointment can either be created by anoymous user, a signed-in customer_user or created by an internal_user when a customer shows up on the physical store.
    appointment_created_by_internal_user = models.ForeignKey(
        InternalUser, on_delete=models.SET_NULL, null=True, related_name='appointment_created_by')  # when null, it means its created by customer user
    appointment_created_at = models.DateTimeField(auto_now_add=True)
    appointment_last_updated_at = models.DateTimeField(auto_now=True)

    @property
    def appointment_full_name(self):
        return f"{self.appointment_first_name} {self.appointment_last_name}"

    class Meta:
        db_table = 'appointments'
        ordering = ['-appointment_id']

    def __str__(self):
        return f"Name: {self.appointment_first_name} {self.appointment_last_name} -Time: {self.appointment_requested_datetime}"


class AppointmentImages(models.Model):
    image_id = models.BigAutoField(primary_key=True)
    appointment = models.ForeignKey(AppointmentRequest, on_delete=models.SET_NULL,
                                    null=True, related_name='appointment_appointmentimages')
    appointment_image = models.FileField(
        upload_to='appointment_images')  # the bucket's subfolder
    uploaded_date = models.DateTimeField(auto_now_add=True)
    image_is_active = models.BooleanField(default=True)

    class Meta:

        db_table = 'appointment_images'
        ordering = ['-image_id']
        verbose_name = 'appointment_image'
        verbose_name_plural = 'appointment_images'

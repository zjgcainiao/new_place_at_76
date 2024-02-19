from .base import models, InternalUser, CustomerUser, RepairOrder, FormattedPhoneNumberField, gettext_lazy as _, uuid

APPT_STATUS_NOT_SUBMITTED = 0
APPT_STATUS_SUBMITTED = 1
APPT_STATUS_CONFIRMED = 2
APPT_STATUS_REJECTED = 3
APPT_STATUS_RESCHEDULED = 4
APPT_STATUS_PORGRESSING = 5
APPT_STATUS_COMPLETED = 10
APPT_STATUS_CANCELLED = -20


class AppointmentRequest(models.Model):
    STATUS_CHOICES = (
        (APPT_STATUS_NOT_SUBMITTED, _('00: Not Submitted')),
        (APPT_STATUS_SUBMITTED, _('Submitted')),
        (APPT_STATUS_CONFIRMED, _('Confirmed')),
        (APPT_STATUS_REJECTED, _('Rejected')),
        (APPT_STATUS_RESCHEDULED, _('Rescheduled')),
        (APPT_STATUS_PORGRESSING, _('Progressing (tracking status via repair order)')),
        (APPT_STATUS_COMPLETED, _('Completed')),
        (APPT_STATUS_CANCELLED, _('Cancelled')),
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
        null=True, blank=True, verbose_name='Requested Appointment Time')
    appointment_confirmed_datetime = models.DateTimeField(
        null=True, blank=True, verbose_name='Confirmed Appointment Time')
    appointment_reason_for_visit = models.PositiveSmallIntegerField(
        choices=REASON_CHOICES, default=0, verbose_name='Reason for visit?')
    appointment_customer_user = models.ForeignKey(
        CustomerUser, on_delete=models.SET_NULL, null=True, verbose_name='your linked user account')
    appointment_first_name = models.CharField(
        max_length=50, null=True, blank=True)
    appointment_last_name = models.CharField(
        max_length=50, null=True, blank=True)
    appointment_phone_number = FormattedPhoneNumberField(
        help_text='we will send updates to this number.')
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
    appointment_status = models.SmallIntegerField(
        choices=STATUS_CHOICES, default=APPT_STATUS_NOT_SUBMITTED, verbose_name='Appointment Status')
    appointment_status_comments = models.CharField(
        max_length=4000, null=True, blank=True)
    appointment_is_active = models.BooleanField(default=True)
    appointment_preferred_contact_method = models.CharField(
        max_length=100, blank=True, null=True)
    appointment_repair_order = models.ForeignKey(
        RepairOrder, on_delete=models.SET_NULL, null=True, related_name='appointment_repair_order')
    appointment_is_converted_to_ro = models.BooleanField(default=False)
    appointment_confirmation_id = models.UUIDField(
        default=uuid.uuid4, editable=False,  verbose_name='Appointment confirmation ID')  # unique=True,
    # appointment can either be created by anoymous user, a signed-in customer_user or created by an internal_user when a customer shows up on the physical store.
    created_by = models.ForeignKey(
        InternalUser, on_delete=models.SET_NULL, null=True, related_name='appointment_created_by')  # when null, it means its created by customer user
    updated_by = models.ForeignKey(
        InternalUser, on_delete=models.SET_NULL, null=True, related_name='appointment_updated_by')  # when null, it means its created by customer user
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def appointment_full_name(self):
        return f"{self.appointment_first_name} {self.appointment_last_name}"

    class Meta:
        db_table = 'appointments'
        ordering = ['-appointment_id']

    def __str__(self):
        return f"Name: {self.appointment_first_name} {self.appointment_last_name} -Time: {self.appointment_requested_datetime}"


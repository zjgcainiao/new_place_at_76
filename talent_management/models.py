from core_operations.models import US_COUNTRY_CODE, NUMBER_OF_DAYS_IN_A_YEAR
from core_operations.models import FormattedPhoneNumberField, YearsOfWorkField
from django.db import models
import re
from datetime import date
from datetime import datetime
from internal_users.models import InternalUser
from django.utils import timezone
from faker import Faker

fake = Faker()

# added on 2023-06-03. common operational models, functions shall be defined in core_operations app.


UNASSIGNED = 'Unassigned'
VISITOR = 'visitor only'
SERVICE_FRONT = 'service advisor'
SERVICE_GARAGE = 'service technican'
TALENT_MANAGEMENT = 'talent management'
ACCOUNTING = 'Accounting'
CODING_MASTERS = 'code masters'
CYBER_SECURITY = 'cyber security'
TRAINEE = 'Trainee'
LEGAL = 'legal'

DEPARTMENTS = ((UNASSIGNED, 'your deparment has not been assigned yet.'),
               (VISITOR, 'visitor group'),
               (SERVICE_FRONT, 'service advisor group'),
               (SERVICE_GARAGE, 'service technican group'),
               (TALENT_MANAGEMENT, 'talent management group'),
               (LEGAL, 'legal group'),
               (TRAINEE, 'trainee group'),
               (CODING_MASTERS, 'code master group'),
               (CYBER_SECURITY, 'cyber security group'),
               )

PAY_TYPE_UNASSIGNED = 0
PAY_TYPE_HOURLY = 1
PAY_TYPE_SALARY = 2
PAY_TYPE_BONUS = 3
PAY_TYPE_INTERNSHIP = 4
PAY_TYPE_OTHER1 = 5
PAY_TYPE_OTHER2 = 6
PAY_TYPES = ((PAY_TYPE_UNASSIGNED, 'unassigned pay type. Must be assigned before the first work day.'),
             (PAY_TYPE_HOURLY, 'hourly'),
             (PAY_TYPE_SALARY, 'salaried'),
             (PAY_TYPE_INTERNSHIP, 'internship'),
             (PAY_TYPE_BONUS, 'bonus pay'),
             (PAY_TYPE_OTHER1, 'pay type other-1'),
             (PAY_TYPE_OTHER2, 'pay type other-2'),
             )

# 2023-05-23 add pay frequency choices
# Weekly – 52 paychecks per year.
# Biweekly – 26 paychecks per year.
# Semi-monthly – 24 paychecks per year.
# Monthly – 12 paychecks per year.
PAY_FREQUENCY_UNDEFINED = 0
PAY_FREQUENCY_DAILY = 1
PAY_FREQUENCY_WEEKLY = 2
PAY_FREQUENCY_BIWEEKLY = 3
PAY_FREQUENCY_SEMIMONTHLY = 4
PAY_FREQUENCY_MONTHLY = 5
PAY_FREQUENCY_SEMIANNUALLY = 6
PAY_FREQUENCY_ANNUALLY = 7
PAY_FREQUENCY_RESERVE1 = 8
PAY_FREQUENCY_RESERVE2 = 9
PAY_FREQUENCY_LIST = ((PAY_FREQUENCY_UNDEFINED, 'pay frequency not defined'),
                      (PAY_FREQUENCY_DAILY, 'daily'),
                      (PAY_FREQUENCY_WEEKLY, 'weekly'),
                      (PAY_FREQUENCY_BIWEEKLY, 'bi-weekly'),
                      (PAY_FREQUENCY_SEMIMONTHLY, 'semi-monthly'),
                      (PAY_FREQUENCY_MONTHLY, 'monthly'),
                      (PAY_FREQUENCY_SEMIANNUALLY, 'monthly'),
                      (PAY_FREQUENCY_ANNUALLY, 'monthly'),
                      (PAY_FREQUENCY_RESERVE1,
                       'reserved pay frequency 1; not used yet'),
                      (PAY_FREQUENCY_RESERVE2,
                       'reserved pay frequency 2; not used yet'),
                      )


class TalentsModel(models.Model):

    talent_id = models.BigAutoField(primary_key=True)
    talent_employee_id = models.IntegerField(unique=True)
    talent_first_name = models.CharField(max_length=50, null=False)
    talent_last_name = models.CharField(max_length=50, null=False)
    talent_middle_name = models.CharField(max_length=50, null=True, blank=True)
    talent_preferred_name = models.CharField(
        max_length=50, null=True, blank=True)
    talent_email = models.EmailField(max_length=50, blank=True, null=True)
    # this custom field works with a glitch as of 2023-06-03.
    talent_phone_number_primary = FormattedPhoneNumberField()
    talent_phone_number_primary_digits_only = models.CharField(
        max_length=20, null=True, blank=True)
    talent_phone_number_alternates_01 = FormattedPhoneNumberField(null=True)
    talent_phone_number_alternates_02 = FormattedPhoneNumberField(null=True)
    talent_emergency_contact = models.CharField(
        max_length=200, null=True, blank=True)
    talent_date_of_birth = models.DateField(
        verbose_name='your date of birth', null=True)

    talent_physical_address_01 = models.CharField(
        verbose_name='street address 01', max_length=100)
    talent_physical_address_02 = models.CharField(
        verbose_name='street address 02(apt numbers, unit #, etc.)', max_length=100, blank=True, null=True)
    talent_physical_address_city = models.CharField(max_length=50, null=True)
    talent_physical_address_state = models.CharField(max_length=2, null=True)
    talent_physical_address_zip_code = models.CharField(
        max_length=10, null=True)
    talent_physical_address_country = models.CharField(
        max_length=50, default='US')
    talent_mailing_address_is_the_same_physical_address = models.BooleanField(
        default=True)
    talent_mailing_address_01 = models.CharField(
        verbose_name='mailing address 01', max_length=100)
    talent_mailing_address_02 = models.CharField(
        verbose_name=' mailing address 02 (apt numbers, unit #, etc)', max_length=100, blank=True, null=True)
    talent_mailing_address_city = models.CharField(max_length=50, null=True)
    talent_mailing_address_state = models.CharField(max_length=2, null=True)
    talent_mailing_address_zip_code = models.CharField(max_length=10)
    talent_mailing_address_country = models.CharField(
        max_length=50, default='US')
    talent_education_level = models.CharField(max_length=100, default='None')
    talent_certifications = models.CharField(
        max_length=500, null=True, blank=True)

    talent_hire_date = models.DateTimeField(blank=True, null=True)
    talent_department = models.CharField(max_length=50,
                                         choices=DEPARTMENTS,
                                         default=UNASSIGNED)
    talent_supervisor = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True)
    talent_work_start_date = models.DateTimeField(blank=True, null=True)
    talent_pay_type = models.PositiveSmallIntegerField(default=PAY_TYPE_UNASSIGNED,
                                                       choices=PAY_TYPES)
    talent_pay_rate = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    talent_pay_frequency = models.PositiveSmallIntegerField(choices=PAY_FREQUENCY_LIST,
                                                            default=PAY_FREQUENCY_UNDEFINED)
    talent_previous_department = models.CharField(max_length=50,
                                                  choices=DEPARTMENTS,
                                                  default=UNASSIGNED,
                                                  )
    talent_discharge_date = models.DateTimeField(null=True, blank=True)
    talent_years_of_work = YearsOfWorkField(null=True, blank=True)
    talent_HR_remarks_json = models.TextField(null=True, blank=True)
    talent_incident_record_json = models.TextField(null=True, blank=True)

    # added on 2023-06-02 to store the future talent_digital_files
    talent_digital_file_storage_path_01 = models.CharField(
        max_length=2000, null=True, blank=True)
    talent_digital_file_storage_path_02 = models.CharField(
        max_length=2000, null=True, blank=True)

    talent_is_active = models.BooleanField(default=True)
    talent_created_at = models.DateTimeField(auto_now_add=True)
    talent_last_udpated_date = models.DateTimeField(auto_now=True)
    talent_created_by_user = models.ForeignKey(
        InternalUser, null=True, on_delete=models.SET_NULL)

    @property
    def talent_full_name(self):
        return f"{self.talent_first_name} {self.talent_last_name} {self.talent_middle_name }"

    @property
    def talent_full_physical_address(self):
        addr_fields = [self.talent_physical_address_01, self.talent_physical_address_02, self.talent_physical_address_city, self.talent_physical_address_state.upper(),
                       self.talent_physical_address_zip_code]

        full_address = " ".join(
            [field for field in addr_fields if field is not None]).strip()
        if len(full_address) != 0:
            full_address = full_address + " " + self.talent_physical_address_country
        else:
            full_address = full_address
        return full_address

    @property
    def talent_full_mailing_address(self):
        addr_fields = [self.talent_mailing_address_01, self.talent_mailing_address_02, self.talent_mailing_address_city, self.talent_mailing_address_state,
                       self.talent_mailing_address_zip_code]
        full_address = " ".join(
            [field for field in addr_fields if field is not None]).strip()

        # if the first 5 fields are empty; do not add the country in the end, return none instead.
        if len(full_address) != 0:
            full_address = full_address + " " + self.talent_mailing_address_country
        else:
            full_address = full_address
        return full_address

    def __str__(self):
        return f"{self.talent_first_name} {self.talent_last_name} {self.talent_middle_name}"

    def save(self, *args, **kwargs):
        # if not self.pk:
        # Only set the talent_created_by_user_id if this is a new instance
        # self.talent_created_by_user_id = request.user.id
        # super(TalentsModel, self).save(*args, **kwargs)

        # creating a employee_id that is different from the talent_id that is used in the database.
        # employee ID start from 1024
        if not self.talent_employee_id:
            last_talent_employee = TalentsModel.objects.order_by(
                '-talent_employee_id').first()
            if last_talent_employee:
                self.talent_employee_id = last_talent_employee.talent_employee_id + 2
            else:
                self.talent_employee_id = 1024

        elif self.talent_employee_id and self.pk:
            self.talent_employee_id = self.talent_employee_id

        super(TalentsModel, self).save(*args, **kwargs)

    @classmethod
    def update_with_dummy_data(cls):
        talents = cls.objects.all()
        for user in talents:
            talent.email = random_email()
            user.first_name = fake.first_name()
            user.last_name = fake.last_name()
            user.phone_number = fake.phone_number()
            user.save()

    class Meta:
        db_table = 'talent_managment'
        ordering = ['-talent_id']


class TalentDocuments(models.Model):
    document_id = models.BigAutoField(primary_key=True)
    talent = models.ForeignKey(
        TalentsModel, on_delete=models.SET_NULL, null=True)
    talent_employment_docs = models.FileField(
        upload_to='2023_talent_employment_docs')
    talent_uploaded_photos = models.ImageField(upload_to='photos')
    uploaded_date = models.DateTimeField(default=timezone.now)
    document_is_active = models.BooleanField(default=True)

    class Meta:

        db_table = 'talent_documents'
        ordering = ['-talent_id']

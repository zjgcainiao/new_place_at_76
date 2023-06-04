from django.db import models
import re
from datetime import date
from datetime import datetime
from internal_users.models import InternalUser
from django.utils import timezone

# constant value across the whole talent_managment app,
# 
NUMBER_OF_DAYS_IN_A_YEAR = 365
US_COUNTRY_CODE = '1'

# custom field. 
# This field will format the phone number into a standard format "+18182234567"
class FormattedPhoneNumberField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 15
        kwargs['null'] = True
        kwargs['blank'] = True

        super().__init__(*args, **kwargs)
    def format_phone_number(self, phone_number):
        # phone_number = getattr(instance, self.attname)
        # Remove all non-digit characters from the phone number
        phone_number_digits = re.sub(r'\D', '', phone_number)

        # If the phone number is missing the country code, assume it's a US number
        if len(phone_number_digits) == 10:
            full_phone_number_digits = US_COUNTRY_CODE + phone_number_digits
            # Format the phone number as "+1 (818) 223-4456"
            return '+{}({}){}-{}'.format(
                full_phone_number_digits[0:1],
                full_phone_number_digits[1:4],
                full_phone_number_digits[4:7],
                full_phone_number_digits[7:11],
            )
        # 2023-05-22 when importing intital data into talent model from 
        # 2023-05-01-talent_management_init.csv, the 1 is added.
        elif len(phone_number_digits) == 11:
            full_phone_number_digits = phone_number_digits
            return '+{}({}){}-{}'.format(
                full_phone_number_digits[0:1],
                full_phone_number_digits[1:4],
                full_phone_number_digits[4:7],
                full_phone_number_digits[7:11],
            )
        else:
            raise ValueError('phone number must be 10 digits long. example: 234-456-3444 or (234)456-3444. The phone number entered is ', phone_number_digits)

    
    def pre_save(self, model_instance, add):
        phone_number = getattr(model_instance, self.attname)
        # model_instance.talent_phone_number_primary
        if phone_number:
            formatted_phone_number = self.format_phone_number(phone_number)
            setattr(model_instance, self.attname, formatted_phone_number)
            return formatted_phone_number
        return super().pre_save(model_instance, add)
    
# custom field 
class YearsOfWorkField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs['max_digits'] = 5
        kwargs['decimal_places'] = 1
        kwargs['null'] = True
        super().__init__(*args, **kwargs)

    def calculate_years_of_work(self, talent_hire_date):
        today = date.today()
        years = (today.days - talent_hire_date.days) / NUMBER_OF_DAYS_IN_A_YEAR

        return round(years, 1)

    def pre_save(self, model_instance, add):
        talent_hire_date = getattr(model_instance, self.attname)

        # when reading the initial data, the talent_hire_date could be empty string ''.
        # '%Y-%m-%d'
        if isinstance(talent_hire_date, str):
            if talent_hire_date:
                talent_hire_date = datetime.strptime(talent_hire_date, '%Y-%m-%d')
            else:
                years_of_work = None
                return years_of_work
        if talent_hire_date:
            years_of_work = self.calculate_years_of_work(talent_hire_date)
            setattr(model_instance, self.attname, years_of_work)
            return years_of_work
        return super().pre_save(model_instance, add)

# Create your models here.
class TalentsModel(models.Model):
    UNASSIGNED = 'Unassigned'
    SERVICE_FRONT = 'service advisor'
    SERVICE_GARAGE = 'service technican'
    TALENT_MANAGEMENT = 'talent management'
    ACCOUNTING = 'Accounting'
    LEGAL = 'legal'
    VISITOR = 'visitor only'

    DEPARTMENTS = ((UNASSIGNED, 'your deparment has not been assigned yet.'),
                   (SERVICE_FRONT, 'service advisor group'),
                   (SERVICE_GARAGE, 'service technican group'),
                   (TALENT_MANAGEMENT, 'talent management group'),
                   (LEGAL, 'legal group'),
                   (VISITOR, 'visitor group'),
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
    PAY_FREQUENCY_LIST = ((PAY_FREQUENCY_UNDEFINED,'pay frequency not defined'),
                          (PAY_FREQUENCY_DAILY, 'daily'),
                          (PAY_FREQUENCY_WEEKLY, 'weekly'),
                          (PAY_FREQUENCY_BIWEEKLY, 'bi-weekly'),
                          (PAY_FREQUENCY_SEMIMONTHLY, 'semi-monthly'),
                          (PAY_FREQUENCY_MONTHLY, 'monthly'),
                          (PAY_FREQUENCY_SEMIANNUALLY, 'monthly'),
                          (PAY_FREQUENCY_ANNUALLY, 'monthly'),
                          (PAY_FREQUENCY_RESERVE1, 'reserved pay frequency 1; not used yet'),
                          (PAY_FREQUENCY_RESERVE2, 'reserved pay frequency 2; not used yet'),
    )

    talent_id = models.BigAutoField(primary_key=True)
    talent_employee_id = models.IntegerField(unique=True)
    talent_first_name = models.CharField(max_length=50, null=False)
    talent_last_name = models.CharField(max_length=50, null=False)
    talent_middle_name = models.CharField(max_length=50, null=True, blank=True)
    talent_preferred_name = models.CharField(max_length=50, null=True, blank=True)
    talent_email = models.EmailField(max_length=50, blank=True, null=True)
    talent_phone_number_primary = FormattedPhoneNumberField(null=True) # models.CharField(max_length=15, null=True, blank=True)
    talent_emergency_contact = models.CharField(max_length=100, null=True, blank=True)
    talent_date_of_birth = models.DateField(verbose_name='your date of birth')

    talent_physical_address_01 = models.CharField(verbose_name='street address 01', max_length=100)
    talent_physical_address_02 = models.CharField(verbose_name='street address 02(apt numbers, unit #, etc.)', max_length=100, blank=True, null=True)
    talent_physical_address_city = models.CharField(max_length=50, null=True)
    talent_physical_address_state = models.CharField(max_length=2, null=True)
    talent_physical_address_zip_code = models.CharField(max_length=10, null=True)
    talent_physical_address_country = models.CharField(max_length=50, default ='US')
    talent_mailing_address_is_the_same_physical_address = models.BooleanField(default=True)
    talent_mailing_address_01 = models.CharField(verbose_name='mailing address 01', max_length=100)
    talent_mailing_address_02 = models.CharField(verbose_name=' mailing address 02 (apt numbers, unit #, etc)', max_length=100, blank=True, null=True)
    talent_mailing_address_city = models.CharField(max_length=50,null=True)
    talent_mailing_address_state = models.CharField(max_length=2, null=True)
    talent_mailing_address_zip_code = models.CharField(max_length=10)
    talent_mailing_address_country = models.CharField(max_length=50, default ='US')
    talent_education_level = models.CharField(max_length=100, default ='UNDEFINED')
    talent_certifications = models.CharField(max_length=500, null=True, blank=True)


    talent_hire_date = models.DateTimeField(blank=True, null=True)
    talent_department = models.CharField(max_length=50,
                                         choices=DEPARTMENTS,
                                         default=UNASSIGNED)
    talent_supervisor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    talent_work_start_date = models.DateTimeField(blank=True, null=True)
    talent_pay_type = models.PositiveSmallIntegerField(default=PAY_TYPE_UNASSIGNED,
                                                       choices=PAY_TYPES)
    talent_pay_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    talent_pay_frequency = models.PositiveSmallIntegerField(choices=PAY_FREQUENCY_LIST,
                                                            default=PAY_FREQUENCY_UNDEFINED)
    talent_previous_department = models.CharField(max_length=50,
                                                  choices=DEPARTMENTS,
                                                  default=UNASSIGNED,
                                                  )
    talent_discharge_date = models.DateTimeField(null=True)
    talent_years_of_work = YearsOfWorkField(null=True)
    talent_HR_remarks_json = models.TextField(null=True, blank=True)
    talent_incident_record_json = models.TextField(null=True, blank=True)

    # added on 2023-06-02 to store the future talent_digital_files
    talent_digital_file_storage_path_01 = models.CharField(max_length=2000, null=True, blank=True)
    talent_digital_file_storage_path_02 = models.CharField(max_length=2000, null=True, blank=True)

    talent_is_active = models.BooleanField(default=True)
    talent_created_at = models.DateTimeField(auto_now_add=True)
    talent_last_udpated_date = models.DateTimeField(auto_now=True)
    talent_created_by_user = models.ForeignKey(InternalUser, null=True, on_delete=models.SET_NULL)


    @property
    def talent_full_name(self):
        return f"{self.talent_first_name} {self.talent_last_name} {self.talent_middle_name }"
    
    @property
    def talent_full_physical_address(self):
        addr_fields = [self.talent_physical_address_01, self.talent_physical_address_02,self.talent_physical_address_city,self.talent_physical_address_state,
                       self.talent_physical_address_zip_code, self.talent_physical_address_country]
        full_address = " ".join([field for field in addr_fields if field is not None]).strip()
        return full_address
    @property
    def talent_full_mailing_address(self):
        addr_fields = [self.talent_mailing_address_01,self.talent_mailing_address_02, self.talent_mailing_address_city,self.talent_mailing_address_state,
                       self.talent_mailing_address_zip_code, self.talent_mailing_address_country]
        full_address = " ".join([field for field in addr_fields if field is not None]).strip()
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
            last_talent_employee = TalentsModel.objects.order_by('-talent_employee_id').first()
            if last_talent_employee:
                self.talent_employee_id = last_talent_employee.talent_employee_id + 2
            else:
                self.talent_employee_id = 1024
        else:
            self.talent_employee_id = 1024

        super(TalentsModel, self).save(*args, **kwargs)
    class Meta:
        db_table = 'talent_managment'
        ordering =['-talent_id']

class TalentDocuments(models.Model):
    document_id = models.BigAutoField(primary_key=True)
    talent = models.ForeignKey(TalentsModel, on_delete=models.SET_NULL, null=True)
    talent_employment_docs = models.FileField(upload_to='2023_talent_employment_docs')
    talent_uploaded_photos = models.ImageField(upload_to='photos')
    uploaded_date = models.DateTimeField(default=timezone.now)
    document_is_active = models.BooleanField(default=True)
    class Meta:
            
        db_table = 'talent_documents'
        ordering =['-talent_id']

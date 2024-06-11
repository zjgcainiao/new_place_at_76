from celery import shared_task
from appointments.models import AppointmentRequest
import logging
from django.db import transaction
from homepageapp.models import CustomersNewSQL02Model as Customer
from django.db.models import Q
from homepageapp.models import EmailsNewSQL02Model, PhonesNewSQL02Model,CustomerEmailsNewSQL02Model, CustomerPhonesNewSQL02Model
from core_operations.utilities import capitalize_first_letters
logger = logging.getLogger('management_scripts')


@shared_task
def process_customer_from_appointment_task(appointment_id):
    """
    Process a customer from a new appointment.

    Args:
        appointment_id (int): The ID of the appointment.

    Returns:
        list: A list of customer pks.

    Raises:
        AppointmentRequest.DoesNotExist: If the appointment with the given ID does not exist.
        Exception: If there is an error while processing the appointment.
    """
    customer_list = []
    logger.info(f"TASK: Processing customer from a new appointment: {appointment_id}")
    try:
        instance = AppointmentRequest.objects.get(appointment_id=appointment_id)
        email_address = instance.appointment_email
        phone_number = instance.appointment_phone_number_digits_only if instance.appointment_phone_number_digits_only else instance.appointment_phone_number
        first_name = capitalize_first_letters(instance.appointment_first_name)
        last_name = capitalize_first_letters(instance.appointment_last_name)
        print(f'In the appontment: email: {email_address}, phone: {phone_number}, first_name: {first_name}, last_name: {last_name}')

        with transaction.atomic():
            email_customers = Customer.objects.filter(emails__email_address=email_address).distinct()
            phone_customers = Customer.objects.filter(
                Q(phones__phone_number_digits_only=phone_number) |
                Q(phones__phone_number=phone_number)
            ).distinct()
            if email_customers.exists():
                logger.info(f"Found existing customer(s) with email: {email_address}")
                customer_list.append([customer.pk for customer in email_customers if customer.pk not in customer_list])
            if phone_customers.exists():
                logger.info(f"Found existing customer(s) with phone: {phone_number}")
                customer_list.append([customer.pk for customer in phone_customers if customer.pk not in customer_list])
            else:
                # If no customer found by email or phone, create new customer
                new_customer = Customer.objects.create(
                    customer_first_name=first_name,
                    customer_last_name=last_name,
                    customer_is_created_from_appointments=True
                )
                # Create email and phone entries
                new_email = EmailsNewSQL02Model.objects.create(email_address=email_address)
                new_phone = PhonesNewSQL02Model.objects.create(phone_number=phone_number)
                # Link email and phone to customer
                CustomerEmailsNewSQL02Model.objects.create(customer=new_customer, email=new_email)
                CustomerPhonesNewSQL02Model.objects.create(customer=new_customer, phone=new_phone)
                new_customer.save()
                customer_list.append(new_customer.pk)

        return customer_list
    except AppointmentRequest.DoesNotExist:
        logger.error(f"Appointment with ID {appointment_id} does not exist.")
    except Exception as e:
        logger.error(f"Failed to process new appointment: {e}")

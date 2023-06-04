from celery import shared_task
from django.core.mail import send_mail
from talent_management.models import TalentsModel
import csv
from io import StringIO

from django.core.mail import EmailMessage
from django.core.mail import get_connection
from django.conf import settings
from django.contrib import messages
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from time import sleep

from core_operations.common_functions import generate_today_date_format, format_string_with_underscore

# created a crontab schedule. The schedule is to allow the task to run every 30 minutes

# schedule, _ = CrontabSchedule.objects.get_or_create(
#     minute='30',
#     hour='*',
#     day_of_week='*',
#     day_of_month='*',
#     month_of_year='*',
# )

# PeriodicTask.objects.create(
#     crontab=schedule,
#     name='Importing contacts',
#     task='proj.tasks.import_contacts',
# )

@shared_task
def send_report_for_active_talents_with_pay_type_0():
    # Query talents that meet the conditions
    # a pay type mus be assigned before the talent's work day.
    talents = TalentsModel.objects.filter(talent_is_active=True, talent_pay_type=0)


    # the csv_data uses a in-memory file object class StringIO().
    # StringIO module is an in-memory file-like object.
    csv_data = StringIO()

    # Create a CSV file with the talent information
    today_date, today_full_datetime = generate_today_date_format()
    if today_date:
        csv_file_path = ''.join([today_date,'pay_type_unassigned_talent_report.csv'])
    else:
        csv_file_path = 'pay_type_unassigned_talent_report.csv'
    
    csv_file_column_header = ['ID', 'Full Name', 'Email', 'Phone Number','Is_Active','Pay Type (0=unassigned)','Department',
                              'Work Start Date']
 
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_file_column_header)
        # writer = csv.writer(csv_data)
        # writer.writerow(['Talent ID', 'Full Name', 'Email'])
        for talent in talents:
            csv_file_data_fields = [talent.talent_id, talent.talent_full_name, talent.talent_email, talent.talent_phone_number_primary, talent.talent_is_active, talent.talent_pay_type, talent.talent_department,
                            talent.talent_work_start_date,]
            writer.writerow(csv_file_data_fields)

    # Send the report via email
    version_number = 'version 2'
    subject = ''.join([today_date, 'Report for Active Talents with Pay Type 0', ' ', version_number])
    subject = format_string_with_underscore(subject)
    # html_content = report
    # message = report
    body = 'Please find the attached report of talents with pay type 0.'
    from_email = "info@76prolubeplus.com"
    recipient_list = ["automan001@76prolubeplus.com"]

    email = EmailMessage(
        subject=subject,
        # body = htm_content,
        body=body,
        from_email=from_email,
        to=recipient_list,
        bcc=[""],
    )

    email.content_subtype = 'html'

    # Attach the CSV file
    email.attach_file(csv_file_path)

    # email.attach('talents_report.csv', csv_data.getvalue(), 'text/csv')

    # use sleep(10) to simulink a long-processing task.
    # sleep(10)

    # Send the email
    email.send()

    # Set the email content type for web browsers
    # However, if you are confident that your recipients can handle an alternative content type, 
    # you can use the content_subtype attribute on the EmailMessage class to change the main content type. 
    # The major type will always be "text", but you can change the subtype.


    # by specifying the connection in EmailMessage() class, the connection remains open while sending one or multiple emails.
    # otherwise, the EmailMessage() uses the default email backend.
    # with get_connection(
    #     host=settings.EMAIL_HOST,
    #     port=settings.EMAIL_PORT,
    #     username=settings.EMAIL_HOST_USER,
    #     password=settings.EMAIL_HOST_PASSWORD,
    #     use_tls=settings.EMAIL_USE_TLS
    #     ) as connection:

    #     subject = request.POST.get("subject")
    #     email_from = settings.EMAIL_HOST_USER
    #     recipient_list = [request.POST.get("email"), ]
    #     message = request.POST.get("message")
    #     messages.add_message(request, messages.SUCCESS, f"email has been sent to {recipient_list}")
    #     EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()

    # Create the email message
    # email = send_mail(subject, message, from_email, recipient_list)

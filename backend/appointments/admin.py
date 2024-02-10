# Register your models here.
from django.contrib import admin

# Register your models here.
from appointments.models import AppointmentRequest, AppointmentImages

# class CustomerAdmin(admin.ModelAdmin):
#     fields = ['customer_id', 'customer_first_name']

admin.site.register(AppointmentImages)
admin.site.register(AppointmentRequest)
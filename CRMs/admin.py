from django.contrib import admin

# Register your models here.

# Register your models here.
from homepageapp.models import CustomersNewSQL02Model, PhonesNewSQL02Model, AddressesNewSQL02Model
from CRMs.models import Ticket, Operator, OperatorNotification

# class CustomerAdmin(admin.ModelAdmin):
#     fields = ['customer_id', 'customer_first_name']


# class OperatorNotificationAdmin(admin.ModelAdmin):
#     filter_horizontal = ('authorized_customers',)


admin.site.register(Ticket)
admin.site.register(Operator)
admin.site.register(OperatorNotification)

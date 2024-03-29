# Register your models here.
from django.contrib import admin

# Register your models here.
from homepageapp.models import CustomersNewSQL02Model, PhonesNewSQL02Model, AddressesNewSQL02Model
from homepageapp.models import RepairOrdersNewSQL02Model

# class CustomerAdmin(admin.ModelAdmin):
#     fields = ['customer_id', 'customer_first_name']


class VehiclesNewSQL02ModelAdmin(admin.ModelAdmin):
    filter_horizontal = ('authorized_customers',)


admin.site.register(CustomersNewSQL02Model)
admin.site.register(PhonesNewSQL02Model)
admin.site.register(AddressesNewSQL02Model)


admin.site.register(RepairOrdersNewSQL02Model)

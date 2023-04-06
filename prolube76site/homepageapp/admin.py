from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import  CustomersNewSQL02Model,PhonesNewSQL02Model, RepairOrdersNewSQL02Model

# class CustomerAdmin(admin.ModelAdmin):
#     fields = ['customer_id', 'customer_first_name']

admin.site.register(CustomersNewSQL02Model)
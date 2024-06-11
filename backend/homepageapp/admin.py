# Register your models here.
from django.contrib import admin

# Register your models here.
from homepageapp.models import CustomersNewSQL02Model, PhonesNewSQL02Model, AddressesNewSQL02Model
from homepageapp.models import RepairOrdersNewSQL02Model
from homepageapp.models import MovingItem, PersonalItem, MovingRequest

# class CustomerAdmin(admin.ModelAdmin):
#     fields = ['customer_id', 'customer_first_name']


class VehiclesNewSQL02ModelAdmin(admin.ModelAdmin):
    filter_horizontal = ('authorized_customers',)


admin.site.register(CustomersNewSQL02Model)
admin.site.register(PhonesNewSQL02Model)
admin.site.register(AddressesNewSQL02Model)

admin.site.register(RepairOrdersNewSQL02Model)


class MovingItemAdmin(admin.ModelAdmin):
    list_display = ['moving_item', ]
    fieldsets = (
        (None, {
            'fields': ('moving_item', )
        }),
        # ('Container Options', {
        #     'fields': ('container',),
        #     'description': "Select a container that is designated to hold items."
        # }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "container":
            kwargs["queryset"] = PersonalItem.objects.filter(
                is_storage_container=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(MovingItem, MovingItemAdmin)


class MovingRequestAdmin(admin.ModelAdmin):
    list_display = ['request_number', 'moved_by', 'move_date', 'status',]
    fieldsets = (
        (None, {
            'fields': ('request_number', 'moved_by', 'move_date', 'status')
        }),
        # ('Container Options', {
        #     'fields': ('container',),
        #     'description': "Select a container that is designated to hold items."
        # }),
    )


admin.site.register(MovingRequest, MovingRequestAdmin)

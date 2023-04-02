
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import InternalUser


class CustomizedUserAdmin(UserAdmin):
    model = InternalUser
    list_display = ('user_id','email', 'user_first_name', 'user_last_name','is_staff', 'user_is_active')
    list_filter = ('email', 'is_staff', 'user_is_active','is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'user_is_active','user_is_admin')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',  'is_staff', 'user_is_active') #'password1', 'password2',
        }),
    )
    search_fields = ('email',)
    ordering = ('user_id',)


admin.site.register(InternalUser, CustomizedUserAdmin)

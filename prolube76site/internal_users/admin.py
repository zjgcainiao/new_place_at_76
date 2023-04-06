
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import InternalUser
from .forms import InternalUserCreationForm, InternalUserChangeForm


class InternalUserAdmin(UserAdmin):
    add_form = InternalUserCreationForm
    form = InternalUserChangeForm
    model = InternalUser
    list_display = ('user_id','email', 'user_first_name', 'user_last_name','is_staff', 'is_superuser','user_is_active','user_created_at')
    list_filter = ('email', 'is_staff', 'user_is_active','is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('user_first_name', 'user_last_name','date_of_birth')}),
        ('Permissions', {'fields': ('is_staff','is_superuser', 'user_is_active','user_is_admin')}),
        ('Important Dates', {'fields': ('user_created_at', 'last_updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2') #'password1', 'password2',
        }),
    )
    search_fields = ('email',)
    ordering = ('user_id',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(InternalUser, InternalUserAdmin)

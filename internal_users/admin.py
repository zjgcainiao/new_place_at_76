
# Register your models here.
from django.contrib.admin import AdminSite
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from internal_users.models import InternalUser
from internal_users.forms import InternalUserCreationForm, InternalUserChangeForm
from internal_users.forms import AdminAuthenticationForm


class InternalUserAdmin(UserAdmin):
    add_form = InternalUserCreationForm
    form = InternalUserChangeForm
    model = InternalUser
    list_display = ('user_id', 'email', 'user_first_name', 'user_last_name',
                    'is_staff', 'is_superuser', 'user_is_active', 'user_created_at')
    list_filter = ('email', 'is_staff', 'user_is_active', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('user_first_name', 'user_last_name',)}),
        ('Permissions', {'fields': ('is_staff',
         'is_superuser', 'user_is_active', 'user_is_admin')}),
        ('Important Dates', {
         'fields': ('user_created_at', 'last_updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            # 'password1', 'password2',
            'fields': ('email', 'password1', 'password2')
        }),
    )
    search_fields = ('email',)
    ordering = ('user_id',)
    filter_horizontal = ('groups', 'user_permissions',)


# admin.site.register(InternalUser, UserAdmin)

# from internal_users.admin import AdminAuthenticationForm

# added on 2023-06-06

class MyAdminSite(AdminSite):
    login_form = AdminAuthenticationForm


my_admin_site = MyAdminSite()

admin.site.register(InternalUser, InternalUserAdmin)
my_admin_site.register(InternalUser, InternalUserAdmin)

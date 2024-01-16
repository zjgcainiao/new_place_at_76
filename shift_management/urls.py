from django.urls import include, path
from shift_management.views import schedule_shift,schedule_dash
app_name = 'shift_management'
urlpatterns = [

    #     path('profile/', fetch_internal_user_dashboard,
    #          name='internal_user_dashboard'),
    path('schedule_shift/', schedule_shift, name='schedule_shift'),
    path('dash/', schedule_dash, name='schedule_dash'),
]

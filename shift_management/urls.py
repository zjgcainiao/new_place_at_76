from django.urls import include, path
from shift_management.views import schedule_shift
app_name = 'shift_management'
urlpatterns = [

    #     path('profile/', fetch_internal_user_dashboard,
    #          name='internal_user_dashboard'),
    path('schedule_shift/', schedule_shift, name='schedule_shift'),
]

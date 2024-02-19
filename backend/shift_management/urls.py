from django.urls import include, path
from shift_management.views import schedule_shift,shift_dash
app_name = 'shift_management'
urlpatterns = [

    #     path('profile/', fetch_internal_user_dashboard,
    #          name='internal_user_dashboard'),
    path('', shift_dash, name='shift_dash'),
    path('schedule_shift/', schedule_shift, name='schedule_shift'),

]

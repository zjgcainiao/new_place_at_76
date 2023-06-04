from django.urls import include, path
from . import views
from formtools.preview import FormPreview
from .forms import AppointmentRequestForm
from .views import AppointmentCreateView, AppointmentPreviewView, AppointmentSuccessView
app_name = 'appointments'
appointment_create_view = AppointmentCreateView.as_view()
appointment_preview_view = FormPreview(AppointmentPreviewView.as_view(form_class=AppointmentRequestForm))
appointment_success_view = AppointmentSuccessView.as_view()

urlpatterns = [
    path('', views.fetch_master_calendar_view, name='appointment-master'),
    path('create', views.appointment_create_view,  name ='appointment-create-view'),
    path('preview', views.appointment_preview_view, name ='appointment-preview-view'),
    path('success', views.appointment_success, name ='appointment-success-view'),

    ## the following three urls are using the class views.
    # path('create', appointment_create_view, name='appointment-create-view'),
    # path('preview/', appointment_preview_view, name='appointment-preview-view'),
    # path('success/', appointment_success_view, name='appointment-success-view'),
]
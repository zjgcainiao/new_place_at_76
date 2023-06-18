from django.urls import include, path
from . import views
from formtools.preview import FormPreview
from appointments.forms import AppointmentRequestForm
from appointments.views import AppointmentCreateView, AppointmentPreviewView, AppointmentSuccessView, AppointmentDetailView
from appointments.views import AppointmentListView
from appointments.views import appointment_image_list, appointment_image_soft_delete
from appointments.views import appointment_get_vehicle_models



app_name = 'appointments'
appointment_create_view = AppointmentCreateView.as_view()
appointment_preview_view = FormPreview(AppointmentPreviewView.as_view(form_class=AppointmentRequestForm))
appointment_success_view = AppointmentSuccessView.as_view()

urlpatterns = [
    path('', AppointmentListView.as_view(), name='appointment_list'),
    path('create/', views.appointment_create_view,  name ='appointment-create-view'),
    path('get_models/<int:make_id>/', views.appointment_get_vehicle_models, name='appointment-get-vehicle-models'),
    path('create/v2', views.AppointmentCreateView.as_view(),  name ='appointment-create-view-v2'),
    path('preview/', views.appointment_preview_view, name ='appointment-preview-view'),
    path('success/', views.appointment_success, name ='appointment-success-view'),
    path('<int:pk>/', AppointmentDetailView.as_view(), name='appointment_detail'),
    path('<int:pk>/images/', appointment_image_list, name='appointment_image_list'),
    path('images/<int:image_id>/delete/', appointment_image_soft_delete, name='appointment_image_delete'),

    ## the following three urls are using the class views.
    # path('create', appointment_create_view, name='appointment-create-view'),
    # path('preview/', appointment_preview_view, name='appointment-preview-view'),
    # path('success/', appointment_success_view, name='appointment-success-view'),
]
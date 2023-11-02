from django.urls import include, path
from appointments import views
from formtools.preview import FormPreview
from appointments.forms import AppointmentCreationForm
from appointments.views import AppointmentCreateView, AppointmentPreviewView, AppointmentSuccessView, AppointmentDetailView
from appointments.views import AppointmentListView, AppointmentDetailByConfirmationIdView
from appointments.views import appointment_image_list, appointment_image_soft_delete
from appointments.views import appointment_get_vehicle_models


app_name = 'appointments'
appointment_create_view = AppointmentCreateView.as_view()
appointment_preview_view = FormPreview(
    AppointmentPreviewView.as_view(form_class=AppointmentCreationForm))
appointment_success_view = AppointmentSuccessView.as_view()

urlpatterns = [
    path('', AppointmentListView.as_view(), name='appointment_list'),
    path('create/', views.appointment_create_view_for_customer,
         name='create_appointment'),
    path('get_models/<int:make_id>/', views.appointment_get_vehicle_models,
         name='appointment-get-vehicle-models'),
    path('create/v2', views.AppointmentCreateView.as_view(),
         name='appointment-create-view-v2'),
    path('<int:pk>/preview/', views.appointment_preview_view,
         name='appointment_preview_view'),
    path('<int:pk>/success/', views.appointment_success,
         name='appointment_success_view'),

    path('<int:pk>/', AppointmentDetailView.as_view(), name='appointment_detail'),
    path('<uuid:appointment_confirmation_id>/',
         AppointmentDetailByConfirmationIdView.as_view(), name='appointment_detail_by_confirmation'),

    path('<int:pk>/images/', appointment_image_list,
         name='appointment_image_list'),
    path('images/<int:image_id>/delete/', appointment_image_soft_delete,
         name='appointment_image_delete'),

]

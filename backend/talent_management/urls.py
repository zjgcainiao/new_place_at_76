from django.urls import include, path
from django.contrib.auth import views as auth_views
from talent_management.views import TalentListView, TalentDetailView, TalentCreateWizardView, TalentCreatePreview, TalentUpdateView, TalentDeleteView
from talent_management.forms import TALENT_CREATE_FORMS, PersonalContactInfoForm
from talent_management.views import send_talent_report_task, talent_document_list, talent_document_soft_delete, SendSampleReportView

app_name = 'talent_management'

urlpatterns = [
    # other URL patterns

    path('', TalentListView.as_view(), name='talent_list'),
    # talent_id is different from talent_employee_id. This setup is intentional. 2023-05-22
    path('<int:pk>/', TalentDetailView.as_view(), name='talent_detail'),
    path('create/', TalentCreateWizardView.as_view(),
         name='talent_create'),
    path('<int:pk>/update/', TalentUpdateView.as_view(),
         name='talent_update'),
    path('<int:pk>/delete/',
         TalentDeleteView.as_view(), name='talent_delete'),

    path('preview/', TalentCreatePreview(PersonalContactInfoForm),
         name='talent_creation_preview'),
    path('<int:pk>/documents/', talent_document_list,
         name='talent_document_list'),

    path('<int:pk>/documents/<int:document_id>/delete/',
         talent_document_soft_delete, name='talent_document_delete'),
    path('tasks/sample-report-view/',
         SendSampleReportView.as_view(), name='send_sample_report_view'),
    path('send-long-processing-report/', send_talent_report_task,
         name='sending_long_processing_report'),

]

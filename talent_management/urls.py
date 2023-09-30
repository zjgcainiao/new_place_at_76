from django.urls import include, path
from django.contrib.auth import views as auth_views
from talent_management.views import TalentListView, TalentDetailView, TalentCreationWizardView, TalentCreationPreview, TalentUpdateView, TalentDeleteView
from talent_management.forms import TALENT_CREATE_FORMS, PersonalContactInfoForm
from talent_management.views import send_talent_report_task, talent_document_list, talent_document_soft_delete

app_name = 'talent_management'

urlpatterns = [
    # other URL patterns

    path('', TalentListView.as_view(), name='talent_list'),
    # talent_id is different from talent_employee_id. This setup is intentional. 2023-05-22
    path('<int:pk>/', TalentDetailView.as_view(), name='talent_detail'),
    path('create/', TalentCreationWizardView.as_view(),
         name='talent_create'),
    path('<int:pk>/update/', TalentUpdateView.as_view(),
         name='talent_update'),
    path('<int:pk>/delete/',
         TalentDeleteView.as_view(), name='talent_delete'),

    path('preview/', TalentCreationPreview(PersonalContactInfoForm),
         name='talent_creation_preview'),
    path('<int:pk>/documents/', talent_document_list,
         name='talent_document_list'),

    path('documents/<int:document_id>/delete/',
         talent_document_soft_delete, name='talent_document_delete'),
    path('send-long-processing-report/', send_talent_report_task,
         name='sending_long_processing_report'),

]

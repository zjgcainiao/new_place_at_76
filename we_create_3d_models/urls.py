from django.urls import include, path
from django.contrib.auth import views as auth_views
from we_create_3d_models.views import engine_model_view

app_name = 'we_create_3d_models'

urlpatterns = [
    # other URL patterns
    path('', engine_model_view, name='sample'),
    # talent_id is different from talent_employee_id. This setup is intentional. 2023-05-22

]
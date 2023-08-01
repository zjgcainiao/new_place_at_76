from django.urls import path
from . import views

app_name = "we_have_ai_helpers"

urlpatterns = [
    path('sloos_pdfs/', views.list_pdfs, name='list_sloos_pdfs'),
]
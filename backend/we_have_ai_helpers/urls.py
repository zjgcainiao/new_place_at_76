from django.urls import path
from we_have_ai_helpers import views

app_name = "we_have_ai_helpers"

urlpatterns = [
    # sloos federal quarterly agency reports
    path('sloos_pdfs/', views.list_pdfs, name='list_sloos_pdfs'),
    path('chatbot/', views.return_simple_chatbot_response, name='chatbot_response'),
]

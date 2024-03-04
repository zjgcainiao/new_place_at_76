from django.urls import path
from we_have_ai_helpers.views import list_pdfs, return_simple_chatbot_response, gemini_chatbot_view

app_name = "we_have_ai_helpers"

urlpatterns = [
    # sloos federal quarterly agency reports
    path('sloos_pdfs/', list_pdfs, name='list_sloos_pdfs'),
    path('chatbot/', return_simple_chatbot_response, name='chatbot_response'),
    path('gemini-chatbot/', gemini_chatbot_view, name='gemini_chatbot_view'),
]

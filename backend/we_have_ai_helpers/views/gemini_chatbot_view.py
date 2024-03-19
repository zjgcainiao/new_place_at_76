import os
from google.cloud import aiplatform
from google.cloud.aiplatform_v1.types import Feature
from django.shortcuts import render, redirect
from django.http import JsonResponse
from we_have_ai_helpers.utilities import call_gemini_api_lite
from we_have_ai_helpers.models import ChatMessage
# A form to collect user input
from we_have_ai_helpers.forms import GeminiChatBotForm
from we_have_ai_helpers.utilities import generate_session_id


def gemini_chatbot_view(request):
    context = {'form': GeminiChatBotForm()}
    session_id = request.session.get('gemini_chat_id')
    if session_id:
        chat_history = ChatMessage.objects.filter(
            session_id=session_id)  # Fetch history
    else:
        chat_history = None
        request.session['gemini_chat_id'] = generate_session_id()  # Create ID

    # ... (Save new messages in your ChatMessage model if needed) ...
    if request.method == 'POST':
        form = GeminiChatBotForm(request.POST)
        if form.is_valid():
            user_question = form.cleaned_data['question']
            # Pass chat history to the API call
            chat, response = call_gemini_api_lite(user_question, chat_history)

            # Retrieve context (recent conversation history)
            context_limit = 3  # Ask up to 3 recent questions
            recent_messages = ChatMessage.objects.order_by(
                '-timestamp')[:context_limit]
            context = [
                f"User: {msg.question}\nGemini: {msg.answer}" for msg in recent_messages]

            # Call Gemini API
            response = call_gemini_api_lite(user_question, context)

            # Store message and response
            ChatMessage.objects.create(question=user_question, answer=response)

            return JsonResponse({'response': response})
        else:
            context['error'] = form.errors  # Pass form errors back if needed
    return render(request, 'we_have_ai_helpers/20_chatbot.html', context)

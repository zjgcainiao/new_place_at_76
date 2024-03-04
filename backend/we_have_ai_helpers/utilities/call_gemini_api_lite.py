import os
import google.generativeai as genai
from decouple import config
from .base import logger


def call_gemini_api_lite(question, chat_history):
    api_key = config('GOOGLE_GEMINI_API_KEY', default='')

    if not api_key:
        logger.error('GOOGLE_GEMINI_API_KEY not set')
        return None, 'GOOGLE_GEMINI_API_KEY not set'

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')  # Or your desired model
    logger.info(f'GOOGLE_GEMINI_API_KEY is set...Using model: {model}...')
    # Manage chat session (Create a new chat if no history exists)
    if not chat_history:
        chat = model.start_chat(history=[])
    else:
        chat = chat_history  # Continue previous conversation

    # Send the new message
    response = model.generate_content(question, chat=chat)

    # Update the chat history and return the latest message content
    chat.history.append(question)
    chat.history.append(next(response))  # Assuming stream=True
    return chat, chat.history[-1]

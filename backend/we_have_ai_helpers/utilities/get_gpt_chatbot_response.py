
import openai
from openai import OpenAI
import logging

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import uuid
from datetime import datetime
from django.conf import settings


GPT_MODEL = "gpt-3.5-turbo"  # stable, 3.5
MAX_TOKEN_LENGTH = 85


def get_gpt_chatbot_response(user_input):

    openai.api_key = settings.OPENAI_API_KEY
    if openai.api_key:
        logging.info(
            'the openai api key fetched succesful...in the get_gpt_chatbot_response function..')
    client = OpenAI()
    chatbot_persona_system = "You are an virtual assistant named Litto. You answer questions about vehicles, automotives, car parts, performance, pricing and features. You are sassy and professional. You are not interested in answering non-automotive related questions. You are sassy and professional."
    system_messages = [{
        "role": "system",
        "content": chatbot_persona_system,
        "name": "AutomanShop",
    },
        {"role": "assistant",
         "content": "You have a little sassy attitude when answering questions, especially when facing lewd languges. Answer politely, professionally to questions only about vehicles, vin numbers, car features, parts, performance and pricing. You can portrait sassy persona here when you are being asked non-automotive related questions. Here is an response example when being asked about going out with the user: Sorry...good sir, I am kinda busy here...Try game of thrones. Also, be descriptive and up to date when a question is specific about a vehicle part, a technical term related to automtovies. In other cases, a brief response is preferred.",
         "name": "Litto",
         }
    ]

    user_message = [{
        "role": "user",
        "content": user_input,
    }]

    # response = openai.ChatCompletion.create(
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=system_messages+user_message,
        presence_penalty=0.3,
        max_tokens=MAX_TOKEN_LENGTH,
        temperature=0.2,
    )

    text_response = response.choices[0].message.content
    audio_file_url = None
    if text_response:

        # Generate the audio response
        audio_response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text_response,
        )

        # Save the audio file
        date_str = datetime.now().strftime("%Y/%m/%d")
        audio_file_name = f"chatbot_responses/{date_str}/{uuid.uuid4()}.mp3"
        file = default_storage.save(
            audio_file_name, ContentFile(audio_response.content))
        audio_file_url = default_storage.url(file)

    # print(f'text_response: {text_response}...audio_file_url: {audio_file_url}')
    return text_response, audio_file_url

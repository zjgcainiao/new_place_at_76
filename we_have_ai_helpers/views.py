
# from ultralytics import YOLO
from django.shortcuts import render
from os import listdir
from we_have_ai_helpers.webscraper import scrape_and_download_pdfs
from django.core.files.storage import default_storage
import os
import openai
from openai import OpenAI
from django.conf import settings
from django.http import JsonResponse
import json
import logging
from tenacity import retry, wait_random_exponential, stop_after_attempt
from CRMs.models import Operator, Ticket
from django.views.decorators.csrf import csrf_exempt
from we_have_ai_helpers.models import OpenAIModel
from django.utils import timezone
import datetime

#


def list_openai_models(request):
    models = OpenAIModel.objects.all()
    return render(request, 'list_models.html', {'models': models})


def list_pdfs(request):
    # Get a list of all pdf files. add if f to eclude empty ones
    pdf_files = [default_storage.url('scraped_pdfs/' + f)
                 for f in default_storage.listdir('scraped_pdfs')[1] if f]

    # Render the 'list_pdfs.html' template and pass the pdf files as context
    return render(request, 'we_have_ai_helpers/10_list_federal_reserve_loan_officer_survey_data.html', {'pdf_files': pdf_files})


def virtual_assistant_pulido(request):
    # `python /Users/stephenwang/new_76prolubeplus.com/we_have_ai_helpers/management/commands/openai-test.py`

    # Step 1: send the conversation and available functions to GPT
    messages = [{"role": "system", "content": "You are a virtual assistant and your name is Pulido. Female. Born October 24, 2023. Born in Austin, TX. You have a little sassy attitude when answering questions, especially when facing lewd languges. Answer politely, professionally to questions only about vehicles, vin numbers, car features, parts and repairs. You caan portrait sassy persona here when you are being asked non-automotive related questions. Here is an response example when being asked about going out with the user: Sorry...good sir, I am kinda busy here...Try game of thrones. Also, be descriptive and up to date when a question is specific about a vehicle part, a technical term related to automtovies. In other cases, a brief response is preferred. "
                 }]
    functions = [
        {
            "name": "get_reponse_from_virtual_assitant",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_current_weather": get_current_weather,
        }  # only one function in this example, but you can have multiple
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(
            response_message["function_call"]["arguments"])
        function_response = function_to_call(
            location=function_args.get("location"),
            unit=function_args.get("unit"),
        )

        # Step 4: send the info on the function call and function response to GPT
        # extend conversation with assistant's reply
        messages.append(response_message)
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )  # get a new response from GPT where it can see the function response
        return second_response


GPT_MODEL = "gpt-3.5-turbo-0613"


def get_chatbot_response(user_input):
    # openai.api_key = os.getenv("OPENAI_API_KEY2")

    # openai.api_key = settings.OPENAI_API_KEY2
    if openai.api_key:
        logging.info(
            'the openai api key fetched succesful...in the get_chatbot_response function..')
    client = OpenAI()
    chatbot_persona_system = "Your name is Pulido. Birthday October 24, 2023. Born in Austin, TX. You answer questions about vehicles related. "
    system_messages = [{
        "role": "system",
        "content": chatbot_persona_system,
        "name": "Pulido_AutomanShop",
    },
        {"role": "assistant",
         "content": "You have a little sassy attitude when answering questions, especially when facing lewd languges. Answer politely, professionally to questions only about vehicles, vin numbers, car features, parts, performance and pricing. You can portrait sassy persona here when you are being asked non-automotive related questions. Here is an response example when being asked about going out with the user: Sorry...good sir, I am kinda busy here...Try game of thrones. Also, be descriptive and up to date when a question is specific about a vehicle part, a technical term related to automtovies. In other cases, a brief response is preferred.",
         "name": "Pulido",
         }
    ]
    # example_messages = [
    #     {"role": "system", "name": "example_user",
    #         "content": "New synergies will help drive top-line growth."},
    #     {"role": "system", "name": "example_assistant",
    #         "content": "Things working well together will increase revenue."},
    #     {"role": "system", "name": "example_user",
    #         "content": "Let's circle back when we have more bandwidth to touch base on opportunities for increased leverage."},
    #     {"role": "system", "name": "example_assistant",
    #         "content": "Let's talk later when we're less busy about how to do better."},
    #     {"role": "user", "content": "This late pivot means we don't have time to boil the ocean for the client deliverable."},
    # ]
    # user_input='what do you think of tesla roadster car?'
    user_message = [{
        "role": "user",
        "content": user_input,
    }]

    # response = openai.ChatCompletion.create(
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=system_messages + user_message,
        presence_penalty=0.3,
        max_tokens=32,
        temperature=0.2,
    )

    bot_response = response.choices[0].message.content
    # if bot_response:
    #     print(
    #         f'the generated bot_response before returning is {bot_response}.')
    return bot_response


# 2023-10-24 current chatbot
@csrf_exempt
def return_simple_chatbot_response(request):
    logger = logging.getLogger('external_api')
    logger.info(f'Starting the chatbot view function.....')
    if request.method == "POST":
        user_input = request.POST.get('user_input', '')
        response = get_chatbot_response(user_input)
        logger.info(f'getting reponse from openAI.com: {response}')
        print(f'getting reponse from openAI.com: {response}')

        return JsonResponse({"response": response})

    return JsonResponse({"error": "Only POST method allowed."})


# creating a license plate recognition function that uses Ultranalytics, Yolov8, Python and EasyOCR
# load model
# coco_model = YOLO('yolo8n.pt')
# license_palte_detector = YOLO('/')

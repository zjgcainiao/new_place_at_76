
import openai
from openai import OpenAI
import logging

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

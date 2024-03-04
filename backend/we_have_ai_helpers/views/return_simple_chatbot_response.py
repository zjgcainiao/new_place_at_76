from .base import JsonResponse, csrf_exempt, logging

from we_have_ai_helpers.utilities import get_chatbot_response

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

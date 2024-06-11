from openai import OpenAI
from .base import JsonResponse,  logging, status
from we_have_ai_helpers.utilities import get_gpt_chatbot_response


# 2023-10-24 current chatbot using ChatGPT 3.5 turbo, the stable version

def return_simple_chatbot_response(request):
    logger = logging.getLogger('external_api')
    logger.info('Starting the chatbot view function.....')

    if request.method == "POST":
        user_input = request.POST.get('user_input', '')
        if not user_input:
            return JsonResponse({"error": "No user input provided."},
                                status=status.HTTP_400_BAD_REQUEST)

        text_response, audio_file_url = get_gpt_chatbot_response(user_input)
        logger.info('text_response: ', text_response,
                    'audio_file_url: ', audio_file_url)
        return JsonResponse({"text_response": text_response,
                             "audio_file_url": audio_file_url}, status=status.HTTP_200_OK)

    return JsonResponse({"error": "Only POST method allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

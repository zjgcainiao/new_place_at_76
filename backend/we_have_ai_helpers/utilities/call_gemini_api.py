from google.cloud import aiplatform
from google.cloud.aiplatform_v1.types import Feature
import os

# Google Cloud Platform (GCP) libraries to interact with the Google Gemini model hosted on Vertex AI.


def call_gemini_api(question, context):
    # Endpoint name should be in the format: projects/PROJECT_ID/locations/LOCATION/endpoints/ENDPOINT_ID
    endpoint_name = os.environ.get('GEMINI_ENDPOINT_NAME')

    client_options = {"api_endpoint": endpoint_name}
    client = aiplatform.gapic.PredictionServiceClient(
        client_options=client_options)
    api_key = os.environ.get('GEMINI_API_KEY')
    # Packages the user's question into a Feature object, which is a format Vertex AI understands.
    instance = Feature(value=question)
    context_list = [Feature(value=c) for c in context]

    parameters = dict(authentication={"type": "API_KEY", "api_key": api_key})
    instances = [instance]
    context = aiplatform.gapic.Features(features=context_list)

    response = client.predict(
        endpoint=endpoint_name, instances=instances, context=context, parameters=parameters
    )

    return response.predictions[0].text

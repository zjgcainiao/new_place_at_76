from .base import logger
from django.http import JsonResponse
from homepageapp.models import LicensePlateSnapShotsPlate2Vin, NhtsaDecodedVin, VinNhtsaApiSnapshots
from apis.serializers import PlateAndVinDataSerializer, VinDataAggregatedSerializer
from django.core.exceptions import ObjectDoesNotExist
from firebase_auth_app.authentication import FirebaseAuthentication
from rest_framework import status
import json
from apis.utilities import trigger_vin_or_license_plate_fetch_tasks
from asgiref.sync import async_to_sync
from rest_framework.response import Response
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view, action

# @require_POST


@api_view(['POST'])
def handle_react_native_vehicle_search_api_view(request):
    # 1. Authenticate with Firebase (extract token from headers, etc.)
    firebase_auth = FirebaseAuthentication()
    user, _ = firebase_auth.authenticate(request)
    if not user:
        return JsonResponse({'error': 'Authentication failed'},
                            status=status.HTTP_401_UNAUTHORIZED)

    data = json.loads(request.body)

    license_plate = data.get('licensePlate')
    state = data.get('state')
    if state:
        state = state.upper()
    # True if license plate search
    is_license_plate_search = bool(license_plate and state)
    if not is_license_plate_search:
        vin = data.get('vin')
    else:
        vin = ''
    logger.info(
        f'react native request is a license plate search request?: {is_license_plate_search}')

    # 3. Attempt initial search:
    try:
        if is_license_plate_search:
            queryset = LicensePlateSnapShotsPlate2Vin.objects.filter(
                license_plate=license_plate, state=state)
        elif vin:
            queryset = NhtsaDecodedVin.objects.filter(vin=vin)
        else:
            return JsonResponse({'error': 'Invalid search parameters'},
                                status=status.HTTP_400_BAD_REQUEST)

        if queryset.exists() and is_license_plate_search:
            serializer = PlateAndVinDataSerializer(queryset, many=True)
            # Ensure data is serializable
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif queryset.exists() and not is_license_plate_search:
            aggregated_data = {'vin': vin}
            serializer = VinDataAggregatedSerializer(aggregated_data)

            return Response(serializer.data, status=status.HTTP_200_OK)

        # need to fetch new data
        else:
            returned_vin, success = async_to_sync(
                trigger_vin_or_license_plate_fetch_tasks)(
                license_plate, state, vin)
            if not success:
                return Response({'error': 'No data found for the given search parameters'},
                                status=status.HTTP_404_NOT_FOUND)
            if is_license_plate_search:
                queryset = LicensePlateSnapShotsPlate2Vin.objects.filter(
                    license_plate=license_plate, state=state)
                serializer = PlateAndVinDataSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                aggregated_data = {'vin': vin}
                serializer = VinDataAggregatedSerializer(aggregated_data)
                return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        # Log the error
        logger.error(f'Error occurred during search: {e}', exc_info=True)
        return Response({'error': 'An unexpected error occurred. Try again later'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

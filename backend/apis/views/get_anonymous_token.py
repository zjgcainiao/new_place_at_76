from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from customer_users.models import CustomerUser
from .base import logger
from apis.models import AnonymousUserSearchCount
from internal_users.models import InternalUser

default_internal_user = InternalUser.objects.get(
    pk=2)  # react_native_app SYSTEM_USER


@api_view(['GET'])
def get_anonymous_token(request):
    # Create a token for a dummy user or a generic token with limited scopes
    # Ensure this dummy user has limited permissions
    dummy_user, created = CustomerUser.objects.get_or_create(
        cust_user_email='react-native-app-user@vindoctor.com')

    # Initialize or reset search count
    if created:
        AnonymousUserSearchCount.objects.create(
            user=dummy_user, search_count=0, created_by=default_internal_user, updated_by=default_internal_user)
    else:
        user_search, _ = AnonymousUserSearchCount.objects.get_or_create(
            customer_user=dummy_user)
        user_search.search_count = 0  # Reset or initialize based on your logic
        user_search.updated_by = default_internal_user
        user_search.save()

    try:
        refresh = RefreshToken.for_user(dummy_user)

        logger.info(f'Anonymous token created for {dummy_user}')
        access_token = str(refresh.access_token)
        return Response({
            'refresh': str(refresh),
            'access': access_token,
        })

    except Exception as e:
        logger.error(f'Error creating anonymous token: {e}', exc_info=True)
        return Response({'error': 'Could not create token due to an internal error.'}, status=500)

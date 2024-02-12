
from internal_users.models import InternalUser
from firebase_auth_app.models import FirebaseUser
from customer_users.models import CustomerUser

class MultipleUserModelMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'uid' in request.session:
            uid = request.session['uid']
            firebase_user = None
            specific_user = None

            try:
                firebase_user = FirebaseUser.objects.get(uid=uid)
            except FirebaseUser.DoesNotExist:
                pass

            if firebase_user:
                # Set base user
                request.firebase_user = firebase_user

                # Check each model to find the specific user
                for user_model in [CustomerUser, InternalUser]:
                    try:
                        specific_user = user_model.objects.get(
                            firebase_user=firebase_user)
                        break
                    except user_model.DoesNotExist:
                        continue

                if specific_user:
                    request.user = specific_user

        response = self.get_response(request)
        return response

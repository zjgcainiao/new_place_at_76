from .base import render, csrf_exempt, json
# this function is NOT finished.
# 2023-06-12
@csrf_exempt
def sign_up_via_gmail_to_backend(request):
    if request.method == 'POST':
        # if isinstance(request.user, CustomerUser):
        #     request.user.
        data = json.loads(request.body)
        firebase_user_uid = data.get('uid')
        firebase_user_email = data.get('email')
        firebase_user_display_name = data.get('display_name')
        firebase_user_token = request.POST.get('token')
        firebase_user_credential = data.get('credential')
        firebase_user = {
            'uid': firebase_user_uid,
            'email': firebase_user_email,
            'display_name': firebase_user_display_name,
            'token': firebase_user_token,
            'credential': firebase_user_credential
        }
        return render(request, 'customer_users/60_customer_user_registration_success_via_gmail.html', firebase_user)
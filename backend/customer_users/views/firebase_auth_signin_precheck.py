
from .base import JsonResponse, json, reverse_lazy, CustomerUser, ObjectDoesNotExist, create_customer_user_from_firebase_auth, reverse, login, CustomerUser, reverse_lazy, JsonResponse, json



def firebase_auth_signin_precheck(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        uid = data.get('uid')
        redirect_url = reverse_lazy('customer_users:customer_user_dashboard')
        try:
            customer_user = CustomerUser.objects.get(
                cust_user_email=email)  # check if the user exists
            print(customer_user)
            if customer_user is not None:
                login(request, customer_user,
                      backend='customer_users.customer_auth_backend.CustomerUserBackend')
            # return redirect('customer_users:customer_user_dashboard')
            return JsonResponse({"status": "OK", "redirect_url": redirect_url}, status=200)
        except ObjectDoesNotExist:  # if user does not exist
            # create a task to create the user
            create_customer_user_from_firebase_auth.delay(uid, email)
            return JsonResponse({"status": "OK", "message": "User does not exist. Task created to register user."}, status=200)
    else:
        return JsonResponse({"status": "FAIL", "message": "Invalid request method."}, status=400)

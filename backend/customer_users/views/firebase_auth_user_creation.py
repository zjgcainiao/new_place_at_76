from .base import render, CustomerUser, redirect, JsonResponse, ObjectDoesNotExist, \
    create_firebase_auth_user, create_customer_user_from_firebase_auth, auth, \
        sync_to_async, login, csrf_exempt, login_required, json, \
        FirebaseUser, reverse_lazy, reverse



# @csrf_exempt
# @login_required(login_url='customer_users:customer_user_login')
def firebase_auth_user_creation(request):
    if request.method == 'POST':
        # if isinstance(request.user, CustomerUser):
        #     request.user.
        data = json.loads(request.body)

        firebase_user_uid = data.get('uid')
        print(f'firebase user uid is {firebase_user_uid}')
        firebase_user_email = data.get('email')
        firebase_user_display_name = data.get('display_name')
        # firebase_user_phone_number = request.POST.get('')
        firebase_user_password = data.get('password')

        # the password shall not be inlcuded in the FirebaseUser model. Use firebase auth to handle authentication.
        # FirebaseUser model
        try:
            firebase_user = FirebaseUser.objects.get(
                firebase_user_email=firebase_user_email)
            firebase_user.firebase_user_display_name = firebase_user_display_name
            firebase_user.firebase_user_uid = firebase_user_uid
            firebase_user.save()
            # create_customer_user_from_firebase_auth.delay(
            #     firebase_user.uuid, firebase_user_password)
            create_customer_user_from_firebase_auth(
                firebase_user.firebase_user_id, firebase_user_password)
            request.user = CustomerUser.objects.get(
                cust_user_email=firebase_user_email)
            return redirect('customer_users:customer_user_registration_success')
            # return JsonResponse({"status": "OK", "message": "User exists."}, status=200)
        except ObjectDoesNotExist:  # if user does not exist
            # create a task to create a record of FirebaseUser
            # then creating a symbolic customer_user instance that links to the new firebaseuser.

            # this is an async way to call the task when celery is available
            # create_firebase_auth_user.delay(
            #     firebase_user_uid, firebase_user_email, firebase_user_display_name, firebase_user_password)
            create_firebase_auth_user(
                firebase_user_uid, firebase_user_email, firebase_user_display_name, firebase_user_password)

            # firebase_user = firebase_user_task.get()
            # if firebase_user is not None:
            #     create_customer_user_from_firebase_auth.delay(firebase_user.uuid, firebase_user_email,firebase_user_password)

            # request.user = CustomerUser.objects.get(cust_user_email=firebase_user_email)
            return redirect('customer_users:customer_user_registration_success')
            # return JsonResponse({"status": "OK", "message": "First Time firebase user. Task created to register user."}, status=200)
    else:
        return JsonResponse({"status": "FAIL", "message": "Invalid request method."}, status=400)

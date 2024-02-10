from celery import shared_task
from customer_users.models import CustomerUser
from firebase_auth_app.models import FirebaseUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from firebase_admin import auth

# @shared_task. use  it when celery can be enabled on azure. recommend azure functions.  

def create_customer_user_from_firebase_auth(firebase_user_id, password):
    # creating a new customer_user based on the uuid of a firebase user.
    firebase_user = FirebaseUser.objects.get(firebase_user_id=firebase_user_id)
    try:
        customer_user = CustomerUser.objects.get(cust_user_email=firebase_user.firebase_user_email)  # try to get the customer_user by 
    except ObjectDoesNotExist:
        customer_user = CustomerUser.objects.create_user(email=firebase_user.firebase_user_email, password=password)

    # pass on display_name, phone number and save to the new customer_user instance.
    if customer_user is not None:
        customer_user.cust_user_first_name = firebase_user.firebase_user_display_name
        customer_user.cust_user_phone_number = firebase_user.firebase_user_phone_number
        customer_user.cust_user_linked_firebaseuser = firebase_user
        customer_user.save()

    return {
        'cust_user_id': customer_user.cust_user_id,
        'firebase_user_uid': firebase_user.firebase_user_uid,
        'cust_user_first_name': customer_user.cust_user_first_name,
    }

# @shared_task. use it when celery can be enabled on azure. recommend azure functions.  
def create_firebase_auth_user(uid, email, display_name):
    try:
        firebase_user = FirebaseUser.objects.create(firebase_user_uid=uid,
                                           firebase_user_email=email, 
                                           firebase_user_display_name=display_name)  # replace with your own fields as necessary
        # create_customer_user_from_firebase_auth.delay(user.uuid, password)  async function 
        create_customer_user_from_firebase_auth(firebase_user.firebase_user_id)

    except IntegrityError:
        raise ValueError('Cannot create a new FirebaseUser instance. There might be an existing user with the same uid or email.')

    return {
        'firebase_user_id': firebase_user.firebase_user_id,
        'firebase_user_email':firebase_user.firebase_user_email,
    }
    # user.save()
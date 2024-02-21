from .base import decode_activation_token_for_customer_user, CustomerUser, redirect, messages, render,logging

# 2023-10-13 added to require a email verification:
# prefer built-in login over FirebaseAuth login at this moment.

def activate_customer_user_account(request, token):

    logger = logging.getLogger('django.request')

    logger.info(f' the JWT token received from activation link is {token}')
    print(f'new customer user token recieved: {token}')
    try:
        decoded_payload = decode_activation_token_for_customer_user(token)

        if not decoded_payload:
            messages.error(
                request, f'Account activation failure. Invalid or Expired Token.')
            return redirect('customer_users:customer_user_login')

        user_id = decoded_payload['user_id']
        email_verified = decoded_payload['email_verified']
        user = CustomerUser.objects.get(pk=user_id)

        logger.info(f'Decoding user token scuccessfull.')
        # print(f'Decoding customer user token scuccessfull.')
        user_id = decoded_payload['user_id']
        email_verified = decoded_payload['email_verified']
        # print(f'email_verified  decoded: {email_verified}')
        # print(f'user_id decoded: {user_id}')
        print(f'current email_verified: {user.cust_user_email_verified}')

        logger.info(f'the decoded user_id is {user_id or None}')
        user = CustomerUser.objects.get(pk=user_id)
        # If email was not verified at the time of token creation, verify now
        if not email_verified and not user.cust_user_email_verified:
            user.cust_user_email_verified = True
            user.save()
            logger.info(f'Activating customer user {user.pk}...')
            print(f'Activating customer user {user.pk}...')
            # url=redirect('customer_users:customer_user_login')
            # print(f'redirecting url is {url}.....new email_verified: {user.cust_user_email_verified}')
            messages.success(
                request, f'Account activation was successful. Thank you for your efforts. You can login now.')
            return redirect('customer_users:customer_user_login')
        elif not email_verified and user.cust_user_email_verified:
            messages.success(request, f'Account {user.pk} had been activated. Email verified.')
            return redirect('customer_users:customer_user_login')
        else:
            messages.error(request, 'error activating account...')
            return redirect('customer_users:customer_user_login')

    except (TypeError, ValueError, OverflowError, CustomerUser.DoesNotExist):
        user = None
        logger.info(
            f'activating customer user was unsuccessful.')
        return render(request, 'customer_users/11_customer_user_activation_invalid.html')

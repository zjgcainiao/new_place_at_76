from .base import render, CustomerUser, messages, redirect


def customer_user_profile_new(request):
    customer_user = None
    # Logic to fetch and display customer-specific dashboard data
    if request.user.is_authenticated and isinstance(request.user, CustomerUser):
        print(f'the user type is {isinstance(request.user, CustomerUser)}')
        # customer_user = request.user
        customer_user = CustomerUser.objects.get(
            pk=request.user.pk)
        if customer_user.cust_user_email_verified:
            return render(request, 'customer_users/20_customer_user_profile_new.html', {'customer_user': customer_user})
        else:
            return render(request, 'customer_users/20_customer_user_profile_new.html', {'customer_user': customer_user})
    else:
        print(
            f'The user type {request.user}is customerUser?:{isinstance(request.user, CustomerUser)}')
        messages.error(
            request, f'you are not authorized to view this page. please login first or try it again.')
        return redirect('customer_users:customer_user_login')

    # return render(request, 'customer_users/51_dashboard_personal_info.html',{'customer_user': customer_user})

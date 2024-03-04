from .base import render, CustomerUser, redirect


def customer_user_profile(request):
    customer_user = None
    # Logic to fetch and display customer-specific dashboard data

    print(f'the user type is {isinstance(request.user, CustomerUser)}')
    # customer_user = request.user
    customer_user = CustomerUser.objects.get(
        pk=request.user.pk)
    if customer_user.cust_user_email_verified:
        return render(request, 'customer_users/20_customer_user_profile.html', {'customer_user': customer_user})
    else:
        return render(request, 'customer_users/20_customer_user_profile.html', {'customer_user': customer_user})

    # return render(request, 'customer_users/51_dashboard_personal_info.html',{'customer_user': customer_user})

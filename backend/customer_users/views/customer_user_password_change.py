

from django.contrib.auth import update_session_auth_hash
from .base import CustomerUser,render, redirect,reverse
from customer_users.forms import CustomerUserPasswordChangeForm

from django.shortcuts import get_object_or_404

def customer_user_password_change(request, user_id):
    """
    Renders the password change page for the customer user.
    """
    user = request.user if request.user else get_object_or_404(CustomerUser, id=request.user)
    if request.method == "POST":
        form = CustomerUserPasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse("customer_user_password_change_done"))
    else:
        form = CustomerUserPasswordChangeForm(user)
    return render(request, "customer_users/30_password_change.html", {"form": form})
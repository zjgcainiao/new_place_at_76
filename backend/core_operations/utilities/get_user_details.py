# get_user_details function is used to get the user details.

def get_user_details(request):
    is_authenticated = request.user.is_authenticated or False

            
    return {
        "is_authenticated": request.user.is_authenticated,
        # Add other user details you need
    }


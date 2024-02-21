# 2023-12-27. this function takes in a request object and returns the client's ip address. 
# ulitity function to get client ip address
def get_client_ip(request):
    """
    Get the client's IP address from the request object.

    Args:
        request (HttpRequest): The request object.

    Returns:
        str: The client's IP address.

    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # In case of proxies, grab the first IP
    else:
        ip = request.META.get('REMOTE_ADDR')  # Direct IP address
    return ip

import datetime
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from core_operations.utilities import anonymize_ip, get_client_ip
from django.core.cache import cache

class SearchLimitMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    async def __call__(self, request):
        # Check if user is on the search page
        if 'search_page_identifier' in request.path:

            ip = anonymize_ip(request.META.get('REMOTE_ADDR', ''))
            # ip = get_client_ip(request)
            cookie_key = 'search_count'
            search_limit = 3  # Limit to 2 searches

            # Increment IP-based counter
            ip_count = cache.get(ip, 0)
            
            cache.set(ip, ip_count + 1, timeout=86400*30)  # Store count with a 24-hour*30 (one month) timeout

            # Increment cookie-based counter
            cookie_count = int(request.COOKIES.get(cookie_key, 0))
            if cookie_count >= search_limit or ip_count >= search_limit:
                return redirect('signup_page_url')  # Redirect to signup page

        response = await self.get_response(request)
        
        # Set/update cookie
        if 'search_page_identifier' in request.path:
            response.set_cookie(cookie_key, str(cookie_count + 1), max_age=86400)
        return response

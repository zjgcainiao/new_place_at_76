from django.shortcuts import redirect
# from core_operations.models import UserSearchCount
from django.urls import reverse
import time
import logging
import cProfile, pstats, io

logger = logging.getLogger('Django')
class SearchLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before the view is called
        response = self.get_response(request)

        # Code to be executed for each request/response after the view is called
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Check if the current request is for the search view
        if request.path == reverse('shops:vin_or_plate_search'):
            # Handle anonymous users
            if not request.user.is_authenticated:
                client_ip = self.get_client_ip(request)
                # session_key = f"search_count_{client_ip}"
                # request.session[session_key] = request.session.get(session_key, 0) + 1
                # if request.session[session_key] > 1:
                    # return redirect('error_page')  # Redirect to an error page or limit page

                # Use session to count searches
                request.session['search_count'] = request.session.get('search_count', 0) + 1
                if request.session['search_count'] > 1:
                    return redirect('error_page')  # Redirect to an error page or limit page

            # Handle authenticated CustomerUser
            else:
                user_search, created = UserSearchCount.objects.get_or_create(user=request.user)
                if user_search.search_count >= 3:
                    return redirect('error_page')  # Redirect to an error page or limit page
                user_search.search_count += 1
                user_search.save()

        return None
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    


class ResponseTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Start profiling
        profiler = cProfile.Profile()
        profiler.enable()

        # Process the request
        response = self.get_response(request)

        # Stop profiling
        profiler.disable()

        # Log response time
        end_time = time.time()
        response_time = end_time - request.start_time
        logging.getLogger("django").info(f"Response time for {request.path}: {response_time:.2f} seconds")

        # Write profiling results to a string stream
        s = io.StringIO()
        sortby = 'cumulative'  # Can be changed to 'time' or other modes
        ps = pstats.Stats(profiler, stream=s).sort_stats(sortby)
        ps.print_stats()

        # Log profiling results
        logger.info("Profiling data:\n" + s.getvalue())

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        request.start_time = time.time()

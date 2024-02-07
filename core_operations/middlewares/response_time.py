import time
from .base import logger
import cProfile, pstats, io

class ResponseTimeMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Initialize start time here
        request.start_time = time.time()
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
        logger.info(f"Response time for {request.path}: {response_time:.2f} seconds")

        # Write profiling results to a string stream
        s = io.StringIO()
        sortby = 'cumulative'  # Can be changed to 'time' or other modes
        ps = pstats.Stats(profiler, stream=s).sort_stats(sortby)
        ps.print_stats()

        # Log profiling results
        logger.info("Profiling data:\n" + s.getvalue())

        return response

    # def process_view(self, request, view_func, view_args, view_kwargs):
    #     request.start_time = time.time()

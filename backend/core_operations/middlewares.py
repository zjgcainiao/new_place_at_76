from django.shortcuts import redirect
# from core_operations.models import UserSearchCount
from django.urls import reverse
import time
import logging
import cProfile, pstats, io

logger = logging.getLogger('Django')


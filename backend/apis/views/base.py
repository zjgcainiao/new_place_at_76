from rest_framework import viewsets, status
from apis.user_permissions import IsInternalUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from core_operations.models import CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE
from django.core.cache import cache
from core_operations.constants import POPULAR_NHTSA_VARIABLE_IDS, POPULAR_NHTSA_GROUP_NAMES
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Case, When, Value, IntegerField
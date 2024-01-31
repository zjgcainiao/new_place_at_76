import re
import logging
import json
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from datetime import datetime, timedelta
from core_operations.constants import CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE, LIST_OF_STATES_IN_US
from apis.api_vendor_urls import NHTSA_API_URL, PLATE2VIN_API_URL
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apis.utilities import fetch_and_save_single_vin_from_nhtsa_api, fetch_single_plate_data_via_plate2vin_api
from django.db import models
from asgiref.sync import sync_to_async
from dashboard.async_functions import fetch_latest_vin_data_from_snapshots, database_sync_to_async
from django.urls import reverse, reverse_lazy
from django.db.models import Q, Prefetch
from django.views.generic import ListView, DetailView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from internal_users.mixins import InternalUserRequiredMixin
from django.views.generic.edit import CreateView, UpdateView,  DeleteView
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models.query import QuerySet


logger = logging.getLogger('django')

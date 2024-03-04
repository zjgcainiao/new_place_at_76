from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
# from homepageapp.models import CustomersNewSQL01Model, VehiclesNewSQL01Model, RepairOrdersNewSQL01Model
from homepageapp.models import CustomersNewSQL02Model, VehiclesNewSQL02Model, RepairOrdersNewSQL02Model, RepairOrderLineItemSquencesNewSQL02Model
from homepageapp.models import CustomerAddressesNewSQL02Model, CustomerEmailsNewSQL02Model, CustomerPhonesNewSQL02Model
from homepageapp.models import lineItemTaxesNewSQL02Model, LineItemsNewSQL02Model, RepairOrderLineItemSquencesNewSQL02Model
from homepageapp.models import NoteItemsNewSQL02Model
from django.views.generic.edit import CreateView, DeleteView, UpdateView
# from django.views.generic import CreateView, FormView, TemplateView
from django.views.generic import ListView, FormView, DetailView, TemplateView
from django.views.generic.edit import ModelFormMixin
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from dotenv import load_dotenv
import pyodbc
# from .serializers import EmailDataSerializer
import json
import os
from dashboard.forms import CustomerUpdateForm
import requests
from django.http import HttpResponse
# from .serializers import *
from django.db.models import Count
from django.core.paginator import Paginator
# from uuid import UUID
from django.utils import timezone
from django.db.models import Max
from django.http import HttpResponseRedirect
from django.db.models import Prefetch
from django.forms import inlineformset_factory
from django.contrib import messages
from decouple import config, Csv
from django.conf import settings
from shops.views import vehicle_search_product
import logging

logger = logging.getLogger('django.request')

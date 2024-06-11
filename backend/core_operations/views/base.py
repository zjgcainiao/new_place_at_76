from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from core_operations.forms import AddressForm
import googlemaps
import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
import json
from django.http import HttpResponse
from io import BytesIO
from rest_framework import status
import qrcode

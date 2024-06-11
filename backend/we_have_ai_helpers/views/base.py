
# from ultralytics import YOLO
from django.utils import timezone
import datetime
from os import listdir
from django.http import JsonResponse
import json
import logging
from django.core.files.storage import default_storage
import os
import openai
from openai import OpenAI
from django.conf import settings

from tenacity import retry, wait_random_exponential, stop_after_attempt
from CRMs.models import Operator, Ticket
from django.views.decorators.csrf import csrf_exempt
from we_have_ai_helpers.models import OpenAIModel

from rest_framework import status
from django.shortcuts import render

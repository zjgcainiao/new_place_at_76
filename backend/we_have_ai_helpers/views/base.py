
# from ultralytics import YOLO
from django.shortcuts import render
from os import listdir
from we_have_ai_helpers.webscraper import scrape_and_download_pdfs
from django.core.files.storage import default_storage
import os
import openai
from openai import OpenAI
from django.conf import settings
from django.http import JsonResponse
import json
import logging
from tenacity import retry, wait_random_exponential, stop_after_attempt
from CRMs.models import Operator, Ticket
from django.views.decorators.csrf import csrf_exempt
from we_have_ai_helpers.models import OpenAIModel
from django.utils import timezone
import datetime

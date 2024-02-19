from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
import holidays
from shift_management.forms import ScheduleShiftForm
from shift_management.models import TimeClock,Shift
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from shift_management.tasks import add_audit_history_record
from core_operations.constants import CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE

us_holidays = holidays.US(years=CURRENT_TIME_SHOW_DATE_WITH_TIMEZONE.year).items()  or {} # Get holidays for current year
holiday_events = [{"title": name, "start": date.isoformat()} for date, name in us_holidays]
holidays_in_json = JsonResponse(holiday_events, safe=False)
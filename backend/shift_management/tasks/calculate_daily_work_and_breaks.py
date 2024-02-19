
from shift_management.models import WorkSession, DailyWorkLog
from celery import shared_task
import logging
from django.db.models import Sum, F, ExpressionWrapper, fields
from datetime import timedelta
from django.db import transaction
from django.http import JsonResponse
import json
logger = logging.getLogger('django.db')

@shared_task
async def calculate_daily_work_and_breaks(talent, date):
    daily_work_log = None
    logger.info(f"Calculating daily work and breaks for {talent} on {date}")
    sessions = WorkSession.objects.filter(
        talent=talent,
        clock_in__date=date
    ).order_by('clock_in')

    total_work = sessions.aggregate(
        total=Sum(ExpressionWrapper(F('clock_out') - F('clock_in'), output_field=fields.DurationField()))
    )['total'] or timedelta(0)

    # Assuming sessions are ordered by clock_in
    total_break = timedelta(0)
    for i in range(len(sessions) - 1):
        gap = sessions[i + 1].clock_in - sessions[i].clock_out
        total_break += gap
    with transaction.atomic():
        daily_work_log, created = DailyWorkLog.objects.update_or_create(
            talent=talent,
            date=date,
            defaults={
                'total_work_hours': total_work,
                'total_break_duration': total_break
            }
        )
        if created:
            logger.info(f"Daily work log created for {talent} on {date}.total_work_hours={total_work}, total_break_duration={total_break}")
        else:
            logger.info(f"Daily work log updated for {talent} on {date}. total_work_hours={total_work}, total_break_duration={total_break}")

    return daily_work_log

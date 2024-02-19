from django.db.models.signals import post_save
from django.dispatch import receiver
from shift_management.models import WorkSession, DailyWorkLog
from shift_management.tasks import calculate_daily_work_and_breaks
from .base import logger

@receiver(post_save, sender=WorkSession)
def log_daily_work_and_breaks(sender, instance, created, **kwargs):
    logger.info("log_daily_work_and_breaks signal triggered: instance={}, created={}".format(instance, created))
    if not created:
        return  # Optionally, skip updates to existing records if desired
    
    talent = instance.talent
    date = instance.clock_in.date()
    
    # Assuming calculate_daily_hours_and_breaks is defined elsewhere
    daily_work_log = calculate_daily_work_and_breaks.delay(talent, date)
    


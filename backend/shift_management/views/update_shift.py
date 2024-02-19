from shift_management.models import Shift
from .base import render, redirect, holiday_events,ContentType,add_audit_history_record

def update_shift(request, shift_id):
    shift_instance = Shift.objects.get(id=shift_id)
    content_type = ContentType.objects.get_for_model(shift_instance)
    add_audit_history_record.delay(
        'updated',
        request.user.id,
        f'Shift updated: {shift_instance.id} by {request.user}',
        shift_instance.id,
        content_type,
            )
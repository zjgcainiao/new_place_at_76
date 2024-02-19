from .base import send_report_for_active_talents_with_pay_type_0, messages, redirect

def send_talent_report_task(request):
    # call the shared task. the task has sleep (20) in order to mimic a long-processing task.
    # send_report_for_active_talents_with_pay_type_0.delay()
    send_report_for_active_talents_with_pay_type_0.apply_async()
    messages.add_message(request, messages.SUCCESS,
                         "your talent_report with pay type = 0 has been generated and sent. ")
    # refresh the same page.
    return redirect('talent_management:talent_list')

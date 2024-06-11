from .base import render, redirect, messages, reverse, \
    logger
from dashboard.forms import MovingRequestForm, \
    MovingItemInlineFormSet, MovingRequestInlineFormset

from homepageapp.models import MovingRequest, MovingItem


# def moving_request_create(request):
#     form = MovingRequestForm()
#     formset = MovingItemFormSet()
#     if request.method == 'POST':
#         form = MovingRequestForm(request.POST)
#         formset = MovingItemFormSet(request.POST)
#     if form.is_valid() and formset.is_valid():
#         # Save the moving request
#         moving_request = form.save()
#         # Save the formset linked to this moving request
#         formset.instance = moving_request
#         formset.save()
#         if formset.is_valid():
#             formset.save()
#             messages.success(
#                 request,
#                 f'successfully to save #{moving_request.request_number}')
#             # Redirect to the moving request dash
#             return redirect('dashbaord:moving_request_dash')

#     return render(request, 'dashboard/112_moving_request_create.html',
#                   {'form': form, 'formset': formset})


def moving_request_create(request):
    request_form = None
    container_formset = None
    if request.method == 'POST':
        moving_request_form = MovingRequestForm(request.POST)
        container_formset = MovingRequestInlineFormset(
            request.POST, instance=None)

        if moving_request_form.is_valid() and container_formset.is_valid():
            moving_request = moving_request_form.save()
            for container_form in container_formset:

                container = container_form.save(commit=False)
                print(f'here is the saved container info:{container} \
                      from container_form: {container_form}')
                container.moving_request = moving_request
                container.save()

                moving_item_formset = MovingItemInlineFormSet(
                    request.POST, instance=container)
                if moving_item_formset.is_valid():
                    moving_item_formset.save()

        #     formset.instance = moving_request
        #     container_instances = container_formset.save()

        #     # For each container, set up an inline formset to add items
        #     for container_instance in container_instances:
        #         item_formset = MovingItemInlineFormSet(
        #             request.POST, instance=container_instance)
        #         if item_formset.is_valid():
        #             item_formset.save()

            messages.success(request, "Moving Request created successfully!")
            return redirect('dashboard:moving_request_detail', pk=moving_request.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        moving_request_form = MovingRequestForm()
        container_formset = MovingRequestInlineFormset(instance=None)

    return render(
        request,
        'dashboard/112_moving_request_create.html',
        {
            'moving_request_form': moving_request_form,
            'container_formset': container_formset,
        }
    )

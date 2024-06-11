from django.shortcuts import render, redirect
# from dashboard.forms import MovingItemForm


def moving_item_create(request):
    if request.method == 'POST':
        form = MovingItemForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or list
            return redirect('dashboard:moving_item_dash')
    else:
        form = MovingItemForm()
    return render(request, 'your_template_name.html', {'form': form})

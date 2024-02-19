
from django.shortcuts import render, redirect
from we_handle_money_stuff.models import GLAccount
from we_handle_money_stuff.forms import GLSubAccountCreateForm

def gl_sub_account_create(request):
    if request.method == 'POST':
        form = GLSubAccountCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('we_handle_money_stuff:gl_account_dash')
    else:
        form = GLSubAccountCreateForm()
    return render(request, 'we_handle_money_stuff/22_gl_sub_account_create.html', {'form': form})
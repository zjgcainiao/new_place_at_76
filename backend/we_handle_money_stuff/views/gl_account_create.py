
from django.shortcuts import render, redirect
from we_handle_money_stuff.models import GLAccount
from we_handle_money_stuff.forms import GLAccountCreateForm

def gl_account_create(request):
    if request.method == 'POST':
        form = GLAccountCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('we_handle_money_stuff:gl_account_dash')
    else:
        form = GLAccountCreateForm()
    return render(request, 'we_handle_money_stuff/32_gl_account_create.html', {'form': form})
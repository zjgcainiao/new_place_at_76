
from .base import render, redirect,login_required, logger, messages
from we_handle_money_stuff.models import GLAccount
from we_handle_money_stuff.forms import GLAccountUpdateForm
@login_required(login_url='internal_users:int_user_login')
def gl_account_update(request, pk):
    gl_account = GLAccount.objects.get(pk=pk)
    if request.method == 'POST':
        form = GLAccountUpdateForm(request.POST, instance=gl_account)
        if form.is_valid():
            gl_account=form.save(commit=False)
            if getattr(request.user,'user_type'):
                if request.user.user_type=='InternalUser':
                    gl_account.updated_by=request.user
                    gl_account.save()
                    messages.success(request, f'GL Account {gl_account.name} updated')
                else:
                    logger.error(f'User {request.user} not allowed to update GL Account')
                    messages.error(request, f'User {request.user} not allowed to update GL Account.')
                    return redirect('we_handle_money_stuff:gl_account_dash')
            return redirect('we_handle_money_stuff:gl_account_dash')
    else:
        form = GLAccountUpdateForm(instance=gl_account)
    return render(request, 'we_handle_money_stuff/33_gl_account_update.html', {'form': form, pk: pk})
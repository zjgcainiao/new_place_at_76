
from .base import render, redirect,login_required, logger, messages
from we_handle_money_stuff.models import GLAccount, GLSubAccount
from we_handle_money_stuff.forms import GLSubAccountUpdateForm
@login_required(login_url='internal_users:int_user_login')
def gl_sub_account_update(request, pk):
    gl_sub_account = GLSubAccount.objects.get(pk=pk)
    if request.method == 'POST':
        form = GLSubAccountUpdateForm(request.POST, instance=gl_sub_account)
        if form.is_valid():
            gl_sub_account=form.save(commit=False)
            if getattr(request.user,'user_type'):
                if request.user.user_type=='InternalUser':
                    gl_sub_account.updated_by=request.user
                    gl_sub_account.save()
                    messages.success(request, f'GL Sub Account {gl_sub_account.name} updated')
                else:
                    logger.error(f'User {request.user} not allowed to update GL Sub Account')
                    messages.error(request, f'User {request.user} not allowed to update GL Sub Account.')
                    return redirect('we_handle_money_stuff:gl_sub_account_dash')
            return redirect('we_handle_money_stuff:gl_sub_account_dash')
    else:
        form = GLSubAccountUpdateForm(instance=gl_sub_account)
    return render(request, 'we_handle_money_stuff/23_gl_sub_account_update.html', {'form': form, pk: pk})
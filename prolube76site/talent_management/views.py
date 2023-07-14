# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.conf import settings
# from internal_users.models import InternalUser
from talent_management.models import TalentsModel
from internal_users.models import InternalUser
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from talent_management.models import TalentDocuments
from django.db.models import Q
import re
from formtools.wizard.views import SessionWizardView
from formtools.wizard.views import NamedUrlSessionWizardView
from formtools.preview import FormPreview
from talent_management.forms import TALENT_CREATE_FORMS, PersonalContactInfoForm, EmploymentInfoForm, RemarkAndCommentsForm
from talent_management.forms import TalentDocumentsForm
from django.http import HttpResponse
from talent_management.tasks import send_report_for_active_talents_with_pay_type_0

class TalentListView(LoginRequiredMixin, ListView):
# the loginrequiredmixin is not added yet
# class TalentListView(ListView):
    model = TalentsModel
    context_object_name = 'talent_list'
    template_name = 'talent_management/10_talent_list.html'
    login_url = '/users/login'

    def get_queryset(self):
        queryset = super().get_queryset().filter(talent_is_active=True).order_by('talent_id')
        # queryset = queryset
        # Check if search query is provided
        # the search bar's name in the html template is 'talent-search-query'
        search_query = self.request.GET.get('q') #'talent-search-query'

        # search_keywords = self.request.GET.get('talent_first_name'), self.request.GET.get('talent_last_name'), self.request.GET.get('talent_email')
        if search_query:
            # Retrieve search query by ID
            # search_query_by_id = self.request.GET.get('talent-search')

            queryset = queryset.filter(
                Q(talent_first_name__icontains=search_query) |
                Q(talent_last_name__icontains=search_query) |
                Q(talent_email__icontains=search_query) |
                Q(talent_phone_number_primary__icontains=search_query)
            )
            # Remove non-digit characters from the search query
            search_query_digits = re.sub(r'\D', '', search_query)
            if len(search_query_digits) == 10:  # and re.match(r'^\d+$', search_query):
                # Format the search query as per the phone number pattern
                search_query_digits = "1" + search_query_digits
                formatted_search_query = '+{}({}){}-{}'.format(
                    search_query_digits[0:1],
                    search_query_digits[1:4],
                    search_query_digits[4:7],
                    search_query_digits[7:11],
                )
                queryset = queryset.filter(talent_phone_number_primary__icontains=formatted_search_query)
            elif len(search_query_digits) == 11:
                formatted_search_query = '+{}({}){}-{}'.format(
                    search_query_digits[0:1],
                    search_query_digits[1:4],
                    search_query_digits[4:7],
                    search_query_digits[7:11],
                )
                queryset = queryset.filter(Q(talent_phone_number_primary__icontains=formatted_search_query))
        return queryset

    def dispatch(self, request, *args, **kwargs):
        # user has to be instance of InternalUser.
        if isinstance(request.user, InternalUser):
            if not (request.user.is_authenticated):
                return self.handle_no_permission()
            # Check if the user has the required user_auth_group
            # this field shall be strictly controlled and logged. CFO and CTO approvals are required.
            if not hasattr(request.user, 'user_auth_group') or request.user.user_auth_group != 3:
                messages.error(request, "You do not have permission to access this page.")
                return render(request, 'talent_management/30_user_has_no_permission.html')
        else: 
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class TalentDetailView(LoginRequiredMixin, DetailView):
    model = TalentsModel
    context_object_name = 'talent'
    template_name = 'talent_management/20_talent_detail.html'
    login_url = '/users/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TalentDocumentsForm()
        return context

    def post(self, request, *args, **kwargs):
        talent = self.get_object()
        form = TalentDocumentsForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.talent = talent
            document.save()
        return self.get(request, *args, **kwargs)
    
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(user=self.request.user)

class TalentCreationPreview(FormPreview):
    form_template = 'talent_management/41_talent_creation_preview.html' #'talent_management/40_talent_creation.html'
    # preview_template = 'talent_management/41_talent_creation_preview.html'

    def done(self, request, cleaned_data):
        # Save the form data or perform any necessary actions
        TalentsModel.objects.create(**cleaned_data)
        # Add a success message
        messages.success(request, "Talent created successfully.")
        return redirect('talent_management:talent_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context variables needed for preview template
        return context

# class TalentCreationWizardView(SessionWizardView):
# alternative way to allow formpreview to show a preview page after its 'done' after all steps
class TalentCreationWizardView(SessionWizardView):
    form_list = [
        ('personal_and_contact_info', PersonalContactInfoForm),
        ('employment_info', EmploymentInfoForm),
        ('remarks_and_comments', RemarkAndCommentsForm),
        ]
    # [PersonalContactInfoForm,EmploymentInfoForm,]
#     [
#     ('personal_and_contact_info', PersonalContactInfoForm),
#     ('employment_info', EmploymentInfoForm),
#     ('remarks_and_comments', RemarkAndCommentsForm),
# ]
    template_name = 'talent_management/40_talent_creation.html'
    preview_template = 'talent_management/41_talent_creation_preview.html'

    def get(self, request, *args, **kwargs):
        try:
            return self.render(self.get_form())
        except KeyError:
            return super().get(request, *args, **kwargs)

    def done(self, form_list, **kwargs):
        print(form_list)
        talent_data = {}
        for form in form_list:
            talent_data.update(form.cleaned_data)
        # # Create the talent record
        # talent = TalentsModel.objects.create(**talent_data)
        talent = TalentsModel(**talent_data)
        # Get the current user
        user = self.request.user
        if user:
            talent.talent_created_by_user = user
        talent.save()

        # Add a success message
        messages.success(self.request, "Talent created successfully.")
        # return redirect("talent_management:talent_list", {'talent': talent})
        return HttpResponse("this form has been submitted successfully.")
        # return render(self.request, 'talent_management/40_talent_creation.html', {
        #     'form_data': [form.cleaned_data for form in form_list],
        # })

    # def get_context_data(self, form, **kwargs):
    #     context = super().get_context_data(form=form, **kwargs)
    #     if self.steps.current == self.steps.current:
    #         context.update({'another_var': True})
    #     return context

# This one uses shared_task
def send_talent_report_task(request):
    # call the shared task. the task has sleep (20) in order to mimic a long-processing task.
    # send_report_for_active_talents_with_pay_type_0.delay()
    send_report_for_active_talents_with_pay_type_0.apply_async()
    messages.add_message(request, messages.SUCCESS, "your talent_report with pay type = 0 has been generated and sent. ")
    # refresh the same page.
    return redirect('talent_management:talent_list')

def talent_document_list(request, pk):
    talent = TalentsModel.objects.get(pk=pk)
    documents = TalentDocuments.objects.filter(document_is_active=True).filter(talent=talent).all()
    return render(request, 'talent_management/90_talent_document_list.html', {'documents': documents, 'talent': talent})

def talent_document_soft_delete(request, document_id):
    document = get_object_or_404(TalentDocuments, document_id=document_id)
    document.document_is_active = False
    document.save()
    messages.add_message(request, messages.INFO, "Document selected has been deleted.")
    return redirect('talent_management:talent_document_list')
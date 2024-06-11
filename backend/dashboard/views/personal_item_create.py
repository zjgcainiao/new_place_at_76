
from .base import CreateView, redirect, messages, reverse_lazy, \
    InternalUserRequiredMixin, timezone, reverse, logger
from dashboard.forms import PersonalItemCreateForm, PersonalItemImageInlineFormSet
from homepageapp.models import PersonalItem
from django.urls import reverse


class PersonalItemCreateView(CreateView, InternalUserRequiredMixin):
    model = PersonalItem
    form_class = PersonalItemCreateForm
    context_object_name = 'item'
    template_name = 'dashboard/102_personal_item_create.html'
    login_url = reverse_lazy('internal_users:internal_user_login')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     if self.request.POST:
    #         # Initialize the formset with the request data to handle submission
    #         context['image_formset'] = PersonalItemImageInlineFormSet(
    #             self.request.POST, self.request.FILES)
    #     else:
    #         # Initialize an empty formset
    #         context['image_formset'] = PersonalItemImageInlineFormSet()
    #     return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # image_formset = PersonalItemImageInlineFormSet(
        #     self.request.POST, self.request.FILES)
        # if image_formset.is_valid():
        # Save the main PersonalItem object
        self.object.save()
        # Associate the images with the newly created PersonalItem object
        # images = image_formset.save(commit=False)
        # for image in images:
        #     image.personal_item = self.object
        #     image.save()

        logger.info(f'A personal item has been created....\
                    self.object.item_category: {self.object.item_category}')
        messages.success(self.request, 'creation success.')
        return redirect('dashboard:personal_item_detail', pk=self.object.pk)

        # # If the formset is not valid, re-render the form with errors
        # context = self.get_context_data()
        # context['form'] = form
        # # context['image_formset'] = image_formset
        # return self.render_to_response(context)

    def get_success_url(self):
        return reverse('dashboard:personal_item_detail', kwargs={'pk': self.object.pk})

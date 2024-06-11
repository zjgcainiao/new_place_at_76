from .base import UpdateView, LoginRequiredMixin, redirect, messages, \
    reverse_lazy, timezone, logger, reverse
from dashboard.forms import PersonalItemUpdateForm, PersonalItemImageInlineFormSet
from homepageapp.models import PersonalItem, PersonalItemImage
from django.core.exceptions import ObjectDoesNotExist
from core_operations.utilities import generate_code128_barcode_lite


class PersonalItemUpdateView(UpdateView, LoginRequiredMixin):
    model = PersonalItem
    form_class = PersonalItemUpdateForm
    template_name = 'dashboard/103_personal_item_update.html'
    context_object_name = 'item'
    success_url = reverse_lazy('dashboard:personal_item_detail')
    login_url = reverse_lazy('internal_users:internal_user_login')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     if self.request.POST:
    #         # Load the formset with data from the request
    #         context['image_formset'] = PersonalItemImageInlineFormSet(
    #             self.request.POST,
    #             self.request.FILES,
    #             instance=self.object
    #         )
    #     else:
    #         # Load existing images in the formset for this PersonalItem
    #         context['image_formset'] = PersonalItemImageInlineFormSet(
    #             instance=self.object)
    #     return context

    def form_valid(self, form):
        # Call the form's save method with `commit=True` to ensure that images are saved
        self.object = form.save(commit=True)
        # image_formset = PersonalItemImageInlineFormSet(
        #     self.request.POST,
        #     self.request.FILES,
        #     instance=self.object)
        # if image_formset.is_valid():
        # Save the updated PersonalItem object
        self.object.save()
        logger.info(
            f'object saved in personal_item_update_view: {self.object}')
        # images = self.object.get('item_images', [])
        # print(f'images captured during form saving function: {images}')
        # for image in images:
        #     PersonalItemImage.objects.create(
        #         personal_item=self.object,
        #         image=image,
        #     )

        # # Save all images associated with this PersonalItem
        # images = image_formset.save(commit=False)
        # for image in images:
        #     image.personal_item = self.object
        #     image.save()

        # # Also delete any images marked for deletion
        # image_formset.save_m2m()

        logger.info(
            f'Personal item has been updated....\
                item category: {self.object.item_category}'
        )
        messages.success(
            self.request, f'Item ID: {self.object.pk} \
                has been successfully updated.'
        )
        return redirect(self.get_success_url())
        # # If the formset is invalid, re-render the form with errors
        # context = self.get_context_data()
        # context['form'] = form
        # context['image_formset'] = image_formset
        # return self.render_to_response(context)

    def get_success_url(self):
        return reverse('dashboard:personal_item_detail', kwargs={'pk': self.object.pk})

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

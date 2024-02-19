from .base import render, redirect, messages, get_object_or_404,reverse, \
    InternalUserRequiredMixin, DetailView, \
    TalentsModel, TalentDocumentForm, TalentDocuments

class TalentDetailView(InternalUserRequiredMixin, DetailView):
    model = TalentsModel
    context_object_name = 'talent'
    template_name = 'talent_management/20_talent_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TalentDocumentForm()
        return context

    def post(self, request, *args, **kwargs):
        talent = self.get_object()
        form = TalentDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.talent = talent
            if request.user.user_type=='InternalUser':
                document.uploaded_by = request.user
            document.save()
            messages.success(request, "Document uploaded successfully.")
            redirect(reverse('talent_management:talent_detail', args=[talent.pk]))
        return self.get(request, *args, **kwargs)

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(user=self.request.user)
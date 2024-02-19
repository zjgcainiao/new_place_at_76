from .base import render, redirect, messages, get_object_or_404, TalentDocuments, reverse


def talent_document_soft_delete(request, pk, document_id):
    document = get_object_or_404(TalentDocuments, document_id=document_id)
    document.document_is_active = False
    document.save()
    messages.add_message(request, messages.INFO,
                         "Document selected has been deleted.")
    return redirect(reverse('talent_management:talent_document_list', kwargs={'pk': pk}))

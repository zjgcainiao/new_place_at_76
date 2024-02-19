from .base import TalentsModel, render, TalentDocuments

def talent_document_list(request, pk):
    talent = TalentsModel.objects.get(pk=pk)
    documents = TalentDocuments.objects.filter(
        document_is_active=True).filter(talent=talent).all()
    return render(request, 'talent_management/90_talent_document_list.html', {'documents': documents, 'talent': talent})
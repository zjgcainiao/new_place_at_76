from .base import forms, TalentDocuments

class TalentDocumentForm(forms.ModelForm):
    class Meta:
        model = TalentDocuments
        fields = ['talent_document']

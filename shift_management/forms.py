from django import forms
from talent_management.models import TalentsModel


class ScheduleShiftForm(forms.Form):
    # This field will be set by the calendar
    date = forms.DateField(widget=forms.HiddenInput())
    start_time = forms.TimeField(help_text="Start time of the shift")
    end_time = forms.TimeField(help_text="End time of the shift")
    assigned_talent = forms.ModelChoiceField(
        queryset=TalentsModel.objects.filter(talent_is_active=True).all(), help_text="Talent assigned to this shift")
    notes = forms.CharField(
        widget=forms.Textarea, required=False, help_text="Any notes for this shift")

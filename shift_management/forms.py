from django import forms
from talent_management.models import TalentsModel
from shift_management.models import Shift
from datetime import time

TIME_CHOICES = [(time(hour, minute), f"{hour:02d}:{minute:02d}")
                for hour in range(24) for minute in [0, 30]]


class ScheduleShiftForm(forms.ModelForm):
    # This field will be set by the calendar
    # date = forms.DateField(widget=forms.HiddenInput())
    date = forms.DateField(widget=forms.DateInput(
        format='%Y-%m-%d',   # Adjust format as needed
        attrs={'type': 'date', 'disabled': True}
    ))
    shift_start_time = forms.ChoiceField(help_text="Start time of the shift", choices=TIME_CHOICES, widget=forms.TimeInput(
        format="%H:%M",  # '14:30',
        attrs={"type": "time"},
    ),)
    shift_end_time = forms.TimeField(
        help_text="End time of the shift", widget=forms.TimeInput(format="%H:%M", attrs={"type": "time"}))

    # shift_duration = forms.ChoiceField(
    #     choices=DURATION_CHOICES, help_text="Duration of the shift")

    shift_talent = forms.ModelChoiceField(
        queryset=TalentsModel.objects.filter(talent_is_active=True).all(), help_text="Talent assigned to this shift", label='Employee worked')
    notes = forms.CharField(
        widget=forms.Textarea, required=False, help_text="Any notes for this shift")

    class Meta:
        model = Shift
        fields = ['shift_start_time', 'shift_end_time',
                  'shift_talent', ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # add a "form-control" class to each form input
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

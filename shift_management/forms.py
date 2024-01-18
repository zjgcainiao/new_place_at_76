from django import forms
from talent_management.models import TalentsModel
from shift_management.models import Shift
from datetime import time
from django.forms.widgets import Select, DateInput, DateTimeInput

TIME_CHOICES = [(time(hour, minute), f"{hour:02d}:{minute:02d}")
                for hour in range(24) for minute in [0, 30]]


class ScheduleShiftForm(forms.ModelForm):
    # This field will be set by the calendar
    # date = forms.DateField(widget=forms.HiddenInput())
    date = forms.DateField(widget=forms.DateInput(
        format='%Y-%m-%d',   # Adjust format as needed
        attrs={'type': 'date', 'disabled': True}
    ))
    start_time = forms.ChoiceField(help_text="Start time of the shift", choices=TIME_CHOICES, widget=forms.TimeInput(
        format="%H:%M",  # '14:30',
        attrs={"type": "time"},
    ),)
    end_time = forms.TimeField(
        help_text="End time of the shift", widget=forms.TimeInput(format="%H:%M", attrs={"type": "time"}))

    # shift_duration = forms.ChoiceField(
    #     choices=DURATION_CHOICES, help_text="Duration of the shift")

    talent = forms.ModelChoiceField(
        queryset=TalentsModel.objects.filter(talent_is_active=True).all(), help_text="Talent assigned to this shift", label='Employee worked')
    note = forms.CharField(
        widget=forms.Textarea, required=False, help_text="Any notes for this shift")

    class Meta:
        model = Shift
        fields = ['start_time', 'end_time',
                  'talent', 'note']
        readonly_fields = ['created_at', 'created_by','updated_at','modified_by']

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # Apply 'form-control' class to all fields by default
            css_class = 'form-control'

            # Specific classes for different field types
            if isinstance(field.widget, Select):
                css_class = 'form-select'  # or any other class for dropdowns
            elif isinstance(field.widget, DateInput):
                css_class = 'form-control datepicker'  # or any other class for date fields
            elif isinstance(field.widget, DateTimeInput):
                css_class = 'form-control datetimepicker'  # or any other class for datetime fields

            # Update the widget attributes
            field.widget.attrs.update({'class': css_class})
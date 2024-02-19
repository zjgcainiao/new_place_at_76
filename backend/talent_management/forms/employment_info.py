from .base import forms, TalentsModel, LIST_OF_STATES_IN_US


class EmploymentInfoForm(forms.ModelForm):
    class Meta:
        model = TalentsModel
        fields = [
            'talent_ssn', 'talent_hire_date', 'talent_department', 'talent_supervisor',
            'talent_pay_type', 'talent_pay_rate', 'talent_pay_frequency',
            # 'talent_previous_department',
            # 'talent_discharge_date','talent_years_of_work',
        ]  # Replace with the actual fields you want to display in the Employment Info section
        widgets = {'talent_hire_date': forms.DateInput(format=('%Y-%m-%d'), attrs={
            'placeholder': 'Select a date',
            'type': 'date',
        }),
            'talent_department': forms.Select(attrs={'class': 'custom-select'}),
            'talent_pay_type': forms.Select(attrs={'class': 'custom-select'}),
            'talent_pay_frequency': forms.Select(attrs={'class': 'form-select'}),
            'talent_pay_rate': forms.NumberInput(attrs={'type': 'text', 'class': 'form-control', }),

        }

        labels = {'talent_pay_rate': 'Pay Rate ($ per hour or per pay cycle)'
                  }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # add a "form-control" class to each form input
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })


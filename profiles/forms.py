from django import forms
from .models import Profile


class DateInput(forms.DateTimeInput):
    input_type = 'date'


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image', 'birth_date', 'sex', 'country', 'work_place', 'degree', 'speciality', 'web_site']

        widgets = {
            'birth_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),
        }

from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'application_type', 'first_name', 'last_name', 'email', 'phone',
            'date_of_birth', 'address', 'city', 'state', 'zip_code', 'country',
            'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship',
            'occupation', 'employer', 'annual_income', 'amount', 'notes'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 4}),
            'annual_income': forms.NumberInput(attrs={'step': '0.01'}),
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
        }

class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status', 'admin_notes']
        widgets = {
            'admin_notes': forms.Textarea(attrs={'rows': 4}),
        }
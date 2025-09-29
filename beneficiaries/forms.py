from django import forms
from .models import Beneficiary, BeneficiaryChangeRequest

class BeneficiaryForm(forms.ModelForm):
    class Meta:
        model = Beneficiary
        fields = [
            'name', 'email', 'phone', 'date_of_birth', 'relationship',
            'address', 'city', 'state', 'zip_code', 'country',
            'percentage', 'is_primary', 'is_active', 'notes'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 4}),
            'percentage': forms.NumberInput(attrs={'step': '0.01', 'max': '100', 'min': '0'}),
        }

class BeneficiaryChangeRequestForm(forms.ModelForm):
    class Meta:
        model = BeneficiaryChangeRequest
        fields = [
            'full_name', 'email', 'current_names', 'new_names',
            'address', 'city', 'state', 'zip_code'
        ]
        widgets = {
            'current_names': forms.Textarea(attrs={'rows': 3}),
            'new_names': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
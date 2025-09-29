from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            'application', 'amount', 'currency', 'payment_method',
            'payer_name', 'payer_email', 'description'
        ]
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class PaymentStatusForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['status', 'transaction_id', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
# forms.py in your Django app

from django import forms
from django.forms import inlineformset_factory
from .models import Sale, SaleItem, Product, Customer

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer', 'date_of_transaction']

SaleItemFormSet = inlineformset_factory(
    Sale, SaleItem, 
    fields=('product', 'quantity'), 
    extra=1, 
    widgets={'product': forms.Select(), 'quantity': forms.NumberInput()}
)

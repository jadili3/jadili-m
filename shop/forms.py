from django import forms
from django.forms import ModelForm, Textarea, TextInput, NumberInput, EmailInput
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class NegotiateForm(forms.Form):
    client_price = forms.CharField(
        label='Your price',
        max_length=100,
        widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Your price'}),
        required=True,
    )

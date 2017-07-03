from django import forms
from registration.forms import RegistrationForm

class UserFormNames(RegistrationForm):
    first_name = forms.CharField(widget=forms.TextInput)
    last_name = forms.CharField(widget=forms.TextInput)
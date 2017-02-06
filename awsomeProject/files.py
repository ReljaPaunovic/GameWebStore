import re
from django import forms
from django.contrib.auth.models import User
from .models import Game
from django.utils.translation import ugettext_lazy as _

# Registration form specification
class RegistrationForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password (again)"))
    isDeveloper = forms.BooleanField(required=False, widget=forms.CheckboxInput, label=_("Developer?"))

    # invoked while checking validity of the form
    def clean_username(self):
        # Raise error if user already exists (the need to be unique)
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))

    # Check if repeated password is the same as other one
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data

# For developers, form for uploading games
class UploadGameForm(forms.Form):
    name = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Name"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    url = forms.URLField(label='Url to game', required=True, widget=forms.TextInput(attrs=dict(required=True, max_length=30)))
    price = forms.FloatField(required=True, min_value=0)
    description = forms.CharField()

    #If game with that name already exists, user is asked to chose another.
    # Game names are unique
    def clean_name(self):
        try:
            game = Game.objects .get(name=self.cleaned_data['name'])
        except Game.DoesNotExist:
            return self.cleaned_data['name']
        raise forms.ValidationError(_("Game name already exists, please chose another one."))

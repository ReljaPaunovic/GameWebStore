import re
from django import forms
from django.contrib.auth.models import User
from .models import Game, UserProfile
from django.utils.translation import ugettext_lazy as _
#from .models import GameImage, ProfileImage
from .models import Photo
import cloudinary, cloudinary.uploader, cloudinary.forms
from django.forms import ModelForm

#class PaymentForm(forms.Form):
'''These stuff here are not to be input by anyone. The parameters are either static (like our SID and the urls) or queried from the data (like the PID and the Amount)
     below 4 lines are not accurate'''
    #pid = forms.RegexField(regex==r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=50)), label=_("Payment ID"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    #sid = forms.RegexField(regex==r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=50)), label=_("Seller ID"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    #amount = forms.FloatField(widget=forms.TextInput(attrs=dict(required=True, max_length=2)), label=_("Amount"), error_messages={ 'invalid': _("The amount must be maximum two decimals and 9 digits")})
    #success_url= forms.URLField(label=_"Success URL")


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
'''
class UploadGameForm(forms.Form):

	name = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Name"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
	url = forms.URLField(label='Url to game', required=True, widget=forms.TextInput(attrs=dict(required=True, max_length=30)))
	price = forms.FloatField(required=True, min_value=0)
	description = forms.CharField()
	image = cloudinary.forms.CloudinaryJsFileField()

	#If game with that name already exists, user is asked to chose another.
	# Game names are unique
	def clean_name(self):
		try:
			game = Game.objects .get(name=self.cleaned_data['name'])
		except Game.DoesNotExist:
			return self.cleaned_data['name']
		raise forms.ValidationError(_("Game name already exists, please chose another one."))
'''
def special_match(strg, search=re.compile(r'[^a-zA-Z0-9 ]').search):
    return not bool(search(strg))

class UploadGameForm(ModelForm):
    class Meta:
        model = Game
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Enter description here.'}),
        }

    def clean_name(self):
        if 'name' in self.cleaned_data:
            if special_match(self.cleaned_data['name']):
                return self.cleaned_data['name']
            else:
                raise forms.ValidationError(_("Name can't contain any special characters"))

class UpdateGameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['url', 'description', 'price']
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Enter description here.'}),
        }

    def clean_name(self):
        if 'name' in self.cleaned_data:
            if re.search(r'\b[a-zA-Z0-9 ]+\b',self.cleaned_data['name']):
                return self.cleaned_data['name']
            else:
                raise forms.ValidationError(_("Name can't contain any special characters"))

'''class DeleteGameForm(ModelForm):
    class Meta:
        model = Game
        fields = '__all__' '''

'''
class UpdateProfileForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("New Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("New Password (again)"))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data
'''
class UpdateProfileForm(ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password (again)"))
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
        }
class UploadPhoto(ModelForm):
	class Meta:
		model = Photo
		exclude = ()

'''
class GameImageForm(ModelForm):
	class Meta:
		model = Photo
		exclude = ()


class ProfileImageForm(ModelForm):
	class Meta:
		model = Photo
		exclude = ()
'''

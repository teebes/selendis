from django import forms
from django.forms.util import ErrorList
from django.contrib.auth.models import User, check_password
from django.contrib.auth.forms import AuthenticationForm

"""
class LoginForm(AuthenticationForm):
    # Inherits from contrib but also allows users to log in with their
    # e-mail address as well as their user name
    username = forms.CharField(label="Account Name or E-Mail Address", max_length=30)
"""

class SaveCharacterForm(forms.Form):
    account_name = forms.CharField(required=True,
                                   help_text="troubleshooting")
    character_name = forms.CharField(required=True)
    email = forms.EmailField(required=False)
    password = forms.CharField(
                        required=True,
                        widget=forms.PasswordInput(render_value=False))
    confirm = forms.CharField(
                        required=True,
                        widget=forms.PasswordInput(render_value=False))
    
    def clean_account_name(self):
        name = self.cleaned_data['account_name']
        if User.objects.filter(username=name):
            raise forms.ValidationError('This account name is taken.')
        return name

    def clean_character_name(self):
        name = self.cleaned_data['character_name']
        if Player.objects.filter(name=name):
            raise forms.ValidationError('This character name is taken.')
        return name
            
    def clean(self):
        data = self.cleaned_data
        if data.has_key('password') and data.has_key('confirm') and \
           data['password'] != data['confirm']:
            self._errors['password'] = ErrorList(["Password and confirm don't match"])
            del data['password']
        return data

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
                            required=True,
                            widget=forms.PasswordInput(render_value=False)
    )
    new_password = forms.CharField(
                            required=True,
                            widget=forms.PasswordInput(render_value=False)
    )
    confirm_password = forms.CharField(
                            required=True,
                            widget=forms.PasswordInput(render_value=False)
    )
    
    def __init__(self, user, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.user = user
    
    def clean_current_password(self):
        password = self.cleaned_data['current_password']
        if not self.user.check_password(password):
            raise forms.ValidationError('Entry for current password is '
                                        'incorrect')
        return password
        
    def clean(self):
        data = self.cleaned_data
        if data.get('new_password')  != data.get('confirm_password'):
            self._errors['new_password'] = ErrorList(["New password and confirm don't match"])
            del data['new_password']
        return data

class ChangeEmailForm(forms.Form):
    email = forms.EmailField(required=True, help_text='teh email')
    password = forms.CharField(
                            required=True,
                            widget=forms.PasswordInput(render_value=False)
    )

    def __init__(self, user, *args, **kwargs):
        super(ChangeEmailForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_password(self):
        password = self.cleaned_data['password']
        if not self.user.check_password(password):
            raise forms.ValidationError('Password is incorrect')
        return password

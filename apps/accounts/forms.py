from django import forms
from django.forms.util import ErrorList
from django.contrib.auth.models import User, check_password

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
            raise forms.ValidationError('Entry for current password is incorrect')
        return password
        
    def clean(self):
        data = self.cleaned_data
        if data.get('new_password')  != data.get('confirm_password'):
            self._errors['new_password'] = ErrorList(["New password and confirm don't match"])
            del data['new_password']
        return data

class ChangeEmailForm(forms.Form):
    email = forms.EmailField(required=True)
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

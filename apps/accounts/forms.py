from django import forms
from django.forms.util import ErrorList
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User, check_password

from stark import config
from stark.apps.accounts.models import Preferences
from stark.apps.anima.models import Player
from stark.apps.world.models import Room

class ChangeEmailForm(forms.Form):
    email = forms.EmailField(required=True,
                             help_text=("A confirmaton e-mail will be sent "
                                        "to the new e-mail address"))
    password = forms.CharField(
                            required=True,
                            widget=forms.PasswordInput(render_value=False),
                            help_text="Enter your current password"
    )

    def __init__(self, user, *args, **kwargs):
        super(ChangeEmailForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_password(self):
        password = self.cleaned_data['password']
        if not self.user.check_password(password):
            raise forms.ValidationError('Password is incorrect')
        return password

class CreateCharacterForm(forms.Form):
    name = forms.CharField(max_length=40)

    def clean_name(self):
        if Player.objects.filter(name=self.cleaned_data['name']):
            raise forms.ValidationError('This character name is taken.')
        return self.cleaned_data['name']

    def save(self, user):
        initial_room = Room.objects.get(pk=getattr(config, 'INITIAL_ROOM', 1))
        player = Player.objects.create(user=user,
                                       name=self.cleaned_data['name'],
                                       status='logged_out',
                                       builder_mode=False,
                                       room=initial_room)

        player.hp = player.max_hp
        player.save()
        player.update_level()

class LoginForm(auth_forms.AuthenticationForm):
    # Inherits from contrib but also allows users to log in with their
    # e-mail address as well as their user name
    username = forms.CharField(label="Account Name or E-Mail Address", max_length=30)

    def clean_username(self):
        username = self.cleaned_data['username']
        users = User.objects.filter(email=username)
        # see if the user input matches an e-mail address
        if len(users) == 1:
            username = users[0].username
        elif len(users) > 1:
            raise Exception("More than one user matched e-mail address %s"
                            % username)
        
        return username

class PreferencesForm(forms.ModelForm):
    class Meta:
        model = Preferences
        exclude = ('user',)


class SaveCharacterForm(forms.Form):
    username = forms.RegexField(
                    label="Account Name",
                    max_length=30,
                    regex=r'^\w+$',
                    help_text = "30 characters or fewer,  alphanumeric "
                                "characters only (letters, digits and "
                                "underscores).",
                    error_message = "This value must contain only letters, "
                                    "numbers and underscores.")
    character_name = forms.CharField(required=True,
                                     help_text="Pick a character name. You "
                                               "can have multiple characters "
                                               "per account.")
    email = forms.EmailField(required=False,
                             help_text="If you want to be able to recover "
                                       "your password or log in as your "
                                       "e-mail address, enter it here or "
                                       "later in your profile.")
    password = forms.CharField(
                        required=True,
                        widget=forms.PasswordInput(render_value=False))
    confirm = forms.CharField(
                        required=True,
                        widget=forms.PasswordInput(render_value=False))
    
    def clean_account_name(self):
        name = self.cleaned_data['username']
        if User.objects.filter(username=name):
            raise forms.ValidationError('This account name is taken.')
        return name

    def clean_character_name(self):
        name = self.cleaned_data['character_name']
        if Player.objects.filter(name=name):
            raise forms.ValidationError('This character name is taken.')
        return name
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if email and User.objects.filter(email=email):
            raise forms.ValidationError("This e-mail address is already "
                                        "registered.")
        return email
        
    def clean(self):
        data = self.cleaned_data
        if data.has_key('password') and data.has_key('confirm') and \
           data['password'] != data['confirm']:
            self._errors['password'] = ErrorList(["Password and confirm don't match"])
            del data['password']
        return data

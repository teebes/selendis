import hashlib
import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, logout as contrib_logout, login as contrib_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm as LoginForm2, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.views import login as login_view

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from stark.apps.anima.models import Player
from stark.apps.accounts.forms import ChangeEmailForm, LoginForm, PreferencesForm, SaveCharacterForm
from stark.apps.accounts.models import EmailConfirmation, Preferences
from stark.apps.accounts.utils import request_confirmation

def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST) # TODO: the fact that the POST data is being passed as a kwarg here seems wrong. But if I don't, nothing works...
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            contrib_login(request, user)
            redirect = request.GET.get('next', None)
            if not redirect:
                redirect = reverse('index')
            return HttpResponseRedirect(redirect)
    else:
        form = LoginForm()
    
    return render_to_response("accounts/login.html", {
        'form': form,
    }, context_instance=RequestContext(request))

def logout(request):
    contrib_logout(request)
    messages.add_message(request, messages.INFO,
                 "You have been logged out.")
    return HttpResponseRedirect(reverse('accounts_login'))

def confirm_email(request, key):
    try:
        confirmation = EmailConfirmation.objects.get(key=key)
    except EmailConfirmation.DoesNotExist:
        raise Http404
    
    confirmation.user.email = confirmation.email
    confirmation.user.save()
    
    EmailConfirmation.objects.filter(email=confirmation.email).delete()

    messages.add_message(request, messages.INFO,
                         "Thank you, your e-mail has been confirmed.")
    
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('accounts_index'))
    else:
        return HttpResponseRedirect(reverse('accounts_login'))

@login_required
def view_account(request):
    players = Player.objects.filter(user=request.user)
    if players.filter(temporary=True):
        # temp players shouldn't be in accounts
        raise Http404

    preferences = Preferences.objects.get(user=request.user)
    preferences_form = PreferencesForm(instance=preferences)
    if request.method == 'POST':
        if request.POST.get('save_preferences'):
            preferences_form = PreferencesForm(request.POST, instance=preferences)
            if preferences_form.is_valid():
                preferences_form.save()
                messages.add_message(request, messages.INFO,
                 "Preferences saved.")
                return HttpResponseRedirect(reverse("accounts_index"))

    return render_to_response("accounts/index.html", {
        'players': Player.objects.filter(user=request.user),
        'preferences_form': preferences_form
    }, context_instance=RequestContext(request))

@login_required
def profile(request):
    # placeholder
    return render_to_response("accounts/profile.html", {
    }, context_instance=RequestContext(request))

@login_required
def change_email(request):
    if request.method == 'POST':
        form = ChangeEmailForm(request.user, request.POST)
        if form.is_valid():
            request_confirmation(request, form.cleaned_data['email'])
            
            request.user.email = 'pending confirmation'
            request.user.save()

            messages.add_message(request,
                                 messages.INFO,
                                 "A confirmation e-mail has been sent to "
                                 "%s. Please click the link inside the mail."
                                 % request.user.email)
            
            return HttpResponseRedirect(reverse('accounts_index'))
    else:
        form = ChangeEmailForm(request.user)

    return render_to_response('accounts/change_email.html', {
        'form': form,
    }, context_instance=RequestContext(request))
    
@login_required
def change_password(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()

            messages.add_message(request,
                             messages.INFO,
                             "Your password has been changed succesfully.")
            
            return HttpResponseRedirect(reverse('accounts_index'))

    return render_to_response('accounts/change_password.html', {
        'form': form,
    }, context_instance=RequestContext(request))

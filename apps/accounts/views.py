import hashlib
import datetime

from django.contrib.auth import authenticate, logout as contrib_logout, login as contrib_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm as LoginForm
from django.contrib.auth.models import User
from django.contrib.auth.views import login as login_view

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from stark.apps.anima.models import Player
from stark.apps.accounts.forms import ChangeEmailForm, ChangePasswordForm, SaveCharacterForm
from stark.apps.accounts.models import EmailConfirmation

def is_temporary(user):
    if len(user.username) >= 5 and user.username[0:5] == 'user_':
        return True
    return False

def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST) # TODO: the fact that the POST data is being passed as a kwarg here seems wrong. But if I don't, nothing works...
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            contrib_login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = LoginForm()
    
    return render_to_response("accounts/login.html", {
        'form': form,
    }, context_instance=RequestContext(request))


@login_required
def save_character(request):
    # only temporary characters can be saved
    if not is_temporary(request.user):
        raise Exception('Only temporary users can be saved')
        
    player = Player.objects.get(user=request.user)
    
    form = SaveCharacterForm()
    if request.method == 'POST':
        form = SaveCharacterForm(request.POST)
        if form.is_valid():
            request.user.username = form.cleaned_data['account_name']
            request.user.set_password(form.cleaned_data['password'])
            request.user.save()
            
            player.name = form.cleaned_data['character_name']
            player.temporary = False
            player.save()
            
            return HttpResponseRedirect(reverse('index'))

    return render_to_response("accounts/save_character.html", {
        'form': form,
        'player': player,
    }, context_instance=RequestContext(request))


def logout(request, login=None):
    contrib_logout(request)
    if login:
        return HttpResponseRedirect(reverse('login'))
    render_to_response('accounts/logout.html', {
    }, context_instance=RequestContext(request))

def confirm_email(request, key):
    # also need a re-send e-mail function
    """
    Stark e-mail confirmation
    Please the confirm the e-mail address you entered on your Stark profile, XXX, is correct by clicking on this link:
    
    XXlinkXXX
    
    Thanks,
    
    The Stark team
    """
    
    # check the token against
    try:
        confirmation = EmailConfirmation.objects.get(key=key)
    except EmailConfirmation.DoesNotExist:
        raise Http404
    
    confirmation.user.email = confirmation.email
    confirmation.user.save()
    
    return HttpResponseRedirect(reverse('accounts/index'))

def generate_email_confirmation_link(user, email):
    # generate hash from date, user and request e-mail
    key = hashlib.sha1("%s%s%s" % (datetime.datetime.now(), user.id, email))
    EmailConfirmation.objects.create(user=user,
                                     email=email,
                                     key=key,
                                     created=datetime.datetime.now())
    # send the email here, use standard template
    # forward to standard page
    

@login_required
def view_account(request):
    return render_to_response("accounts/index.html", {
        'players': Player.objects.filter(user=request.user),
    }, context_instance=RequestContext(request))

@login_required
def change_email(request):
    form = ChangeEmailForm(request.user)
    if request.method == 'POST':
        form = ChangeEmailForm(request.user, request.POST)
        if form.is_valid():
            request.user.email = form.cleaned_data['email']
            request.user.save()
        return HttpResponseRedirect(reverse('accounts_index'))
    return render_to_response('accounts/change_email.html', {
        'form': form,
    }, context_instance=RequestContext(request))
    
@login_required
def change_password(request):
    form = ChangePasswordForm(request.user)
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['new_password'])
            return HttpResponseRedirect(reverse('accounts_index'))
    return render_to_response('accounts/change_password.html', {
        'form': form,
    }, context_instance=RequestContext(request))

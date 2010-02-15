from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from stark.apps.accounts.forms import CreateCharacterForm, SaveCharacterForm
from stark.apps.accounts.models import EmailConfirmation
from stark.apps.accounts.utils import request_confirmation
from stark.apps.anima.models import Player

def is_temporary(user):
    if len(user.username) >= 5 and user.username[0:5] == 'user_':
        return True
    return False

@login_required
def create_character(request):
    if request.method == 'POST':
        form = CreateCharacterForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect(reverse('accounts_index'))
    else:
        form = CreateCharacterForm()
    return render_to_response("accounts/create_character.html", {
        'form': form,
    }, context_instance=RequestContext(request))

@login_required
def enter_realm(request, character=None):
    # log all characters first
    Player.objects.filter(user=request.user).update(status='logged_out')
    character = Player.objects.get(user=request.user, name=character)
    character.status = 'logged_in'
    character.save()
    return HttpResponseRedirect(reverse('index'))

@login_required
def exit_realm(request):
    # even though only one player should be logged on at a time, we log
    # all players off to be safe
    Player.objects.filter(user=request.user).update(status='logged_out')
    return HttpResponseRedirect(reverse("accounts_index"))
    
@login_required
def save_character(request):
    # only temporary characters can be saved
    if not is_temporary(request.user):
        raise Exception('Only temporary users can be saved')
        
    player = Player.objects.get(user=request.user)
    
    form = SaveCharacterForm()
    if request.method == 'POST':
        form = SaveCharacterForm(data=request.POST)
        if form.is_valid():
            # start the e-mail confirmation process if necessary
            email = form.cleaned_data['email']
            if email:
                request_confirmation(request, form.cleaned_data['email'])
                email = 'pending confirmation'

            # create the account
            request.user.username = form.cleaned_data['username']
            request.user.set_password(form.cleaned_data['password'])
            request.user.email = email            
            request.user.save()

            # save the character
            player.name = form.cleaned_data['character_name']
            player.temporary = False
            player.save()

            return HttpResponseRedirect(reverse('accounts_index'))

    return render_to_response("accounts/save_character.html", {
        'form': form,
        'player': player,
        'temporary_user': True,
    }, context_instance=RequestContext(request))
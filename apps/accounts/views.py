import hashlib
import datetime

from django.contrib.auth import authenticate, logout as contrib_logout, login as contrib_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from stark.apps.anima.models import Player
from stark.apps.accounts.forms import ChangeEmailForm, ChangePasswordForm

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

import hashlib
import datetime

from django import forms
from django.contrib.auth import authenticate, logout as contrib_logout, login as contrib_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms.util import ErrorList
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from stark.apps.world.models import Room
from stark.apps.anima.models import Player, MobLoader
from stark import config

def is_temporary(user):
    if len(user.username) >= 5 and user.username[0:5] == 'user_':
        return True
    return False

def index(request):
    initial_room = Room.objects.get(pk=getattr(config, 'INITIAL_ROOM', 1))
    if not request.user.is_authenticated():
        """
        To promote new users, the site automatically creates a throwaway
        user for each unauthenticated visitor. If they've had a good time
        they can change the name and set the password to make it a
        permanent user
        """
        user = User()
        user.save()
        user.username = u"user_%s" % user.id
        temp = hashlib.new('sha1')
        temp.update(str(datetime.datetime.now()))
        password = temp.hexdigest()
        user.set_password(password)
        user.save()
        authenticated_user = authenticate(username=user.username,
                                          password=password)
        contrib_login(request, authenticated_user)
        print initial_room
        player = Player.objects.create(user=user,
                                       name=user.username,
                                       temporary=True,
                                       status='logged_in',
                                       room=initial_room)
        player.update()
        
    else:
        # if the user is already authenticated, get or create their player
        player, created = Player.objects.get_or_create(
                                user=request.user,
                                status='logged_in',
                                name=request.user.username,
                                defaults={'room': initial_room})
        
        if created:
            # if new user, give them builder mode if they're staff
            if request.user.is_staff:
                player.builder_mode = True
                player.save()
            player.update()

    temporary_user = len(request.user.username) >= 5 and \
                     request.user.username[0:5] == 'user_'

    return render_to_response("game/index.html", {
        'player': player,
        'temporary_user': temporary_user,
        }, context_instance=RequestContext(request))

def login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None and user.is_active:
            contrib_login(request, user)
            return HttpResponseRedirect(reverse('index'))
    
    return render_to_response("accounts/login.html", {
    }, context_instance=RequestContext(request))

@login_required
def save_character(request):
    # only temporary characters can be saved
    if not is_temporary(request.user):
        raise Exception('Only temporary users can be saved')
        
    player = Player.objects.get(user=request.user)
    
    class SaveForm(forms.Form):
        account_name = forms.CharField(required=True)
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
    
    form = SaveForm()
    if request.method == 'POST':
        form = SaveForm(request.POST)
        if form.is_valid():
            request.user.username = form.cleaned_data['account_name']
            request.user.set_password(form.cleaned_data['password'])
            request.user.save()
            
            player.name = form.cleaned_data['character_name']
            player.temporary = False
            player.save()
            
            return HttpResponseRedirect(reverse('index'))
        print 'here'

    return render_to_response("accounts/save_character.html", {
        'form': form,
        'player': player,
    }, context_instance=RequestContext(request))

@login_required
def view_account(request):
    return render_to_response("accounts/view_account.html", {
        'players': Player.objects.filter(user=request.user),
    }, context_instance=RequestContext(request))

def logout(request, login=None):
    contrib_logout(request)
    if login:
        return HttpResponseRedirect(reverse('login'))
    return render_to_response("accounts/logout.html", {
    }, context_instance=RequestContext(request))

def quick(request):
    return HttpResponse(request.user.username)

    
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

from stark import config
from stark.apps.anima.models import Player, MobLoader
from stark.apps.world.models import Room
from stark.apps.anima.utils import set_default_aliases
from stark.utils.adx import analyze

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

        player = Player.objects.create(user=user,
                                       name=user.username,
                                       temporary=True,
                                       status='logged_in',
                                       room=initial_room)
        player.hp = player.max_hp
        player.save()
        player.update_level()
        set_default_aliases(player)
        
    else: # returning user
        characters = Player.objects.filter(user=request.user)
        if characters.count() == 0: # no characters, create one
            # new player
            
            # if the user is staff, give the character builder mode
            if request.user.is_staff:
                builder_mode = True
            else:
                builder_mode = False
                
            # if the user's name is already a character name, give a temp name
            character_name = request.user.username
            if characters.filter(name=character_name):
                name = "user_%s" % request.user.id
                
            player = Player.objects.create(user=request.user,
                                           name=character_name,
                                           status='logged_in',
                                           builder_mode=builder_mode,
                                           room=initial_room)
            player.hp = player.max_hp
            player.save()
            player.update_level()
            set_default_aliases(player)
        elif characters.filter(status='logged_in').count() == 1:
            player = characters.get(status='logged_in')
        else:
            characters.update(status='logged_out')
            return HttpResponseRedirect(reverse('accounts_index'))

    return render_to_response("game/index.html", {
        'player': player,
        'temporary_user': player.temporary,
        }, context_instance=RequestContext(request))

def adx(request, input):
    try:
        a, x = input.split('d')
        result = analyze(a, x)
        return HttpResponse(result)
    except Exception:
        return HttpResponse("error")

def quick(request):
    if request.user.is_authenticated():
        return HttpResponse("logged in")
    return HttpResponse("logged out")

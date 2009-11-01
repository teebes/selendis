from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from stark.apps.world.models import Room
from stark.apps.anima.models import Player

@login_required
def index(request):
    return render_to_response("index.html", {
        }, context_instance=RequestContext(request))
   
def quick(request):
    return render_to_response('quick.html')
    
"""
render_
"""
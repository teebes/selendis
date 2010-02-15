from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('stark.apps.preferences.views',
    url(r'^$', 'index', name='preferences_index'),
)
from django.conf import settings
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^stark/', include('stark.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^api/', include('stark.api.urls')),

    url(r'^accounts/', include('stark.apps.accounts.urls')),

    url(r'^$', 'stark.views.index', name='index'),
    url(r'^m/$', 'stark.views.mobile', name='mobile'),

    url(r'^help/$', 'django.views.generic.simple.direct_to_template', {
        'template': 'game/help.html'
        }, name='help'),

    (r'^adx/(?P<input>.*)/$', 'stark.views.adx'),
    (r'^quick/$', 'stark.views.quick'),
    (r'^disrupt/$', 'django.views.generic.simple.direct_to_template', {'template': 'disrupt.html'}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': "%s/static" % settings.SITE_FS_ROOT}),
    )

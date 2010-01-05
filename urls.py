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

    url(r'^$', 'stark.views.index', name='index'),
    
    url(r'^login/$', 'stark.views.login', name='login'),
    url(r'^save/$', 'stark.views.save_character', name='save_character'),
    url(r'^profile/$', 'stark.views.view_account', name='view_account'),
    url(r'^logout/$', 'stark.views.logout', name='logout'),
    url(r'^logout-login/$', 'stark.views.logout', {'login': True}, name='logout-login'),
    
    (r'^quick/$', 'stark.views.quick'),
    (r'^disrupt/$', 'django.views.generic.simple.direct_to_template', {'template': 'disrupt.html'}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': "%s/static" % settings.SITE_FS_ROOT}),
    )

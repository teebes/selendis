from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('stark.apps.accounts.views',
    url(r'^$', 'view_account', name='accounts_index'),
    url(r'^confirm_email/(\w+)/$', 'confirm_email', name='confirm_email'),
    url(r'^change_email/$', 'change_email', name='accounts_change_email'),
    url(r'^change_password/$', 'change_password', name='accounts_change_password'),

    url(r'^profile/$', 'profile', name='accounts_profile'), # placeholder

    url(r'^login/$', 'login', name='accounts_login'),
    url(r'^logout/$', 'logout', name='logout'),

)

urlpatterns += patterns('stark.apps.accounts.views.characters',
    url(r'^create_character/$', 'create_character', name='create_character'),
    url(r'^save/$', 'save_character', name='save_character'),
    url(r'exit/', 'exit_realm', name='exit_realm'),
    url(r'^enter/(?P<character>\w+)/$', 'enter_realm', name='enter_realm'),
)
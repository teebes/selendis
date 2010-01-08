from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('stark.apps.accounts.views',
    url(r'^$', 'view_account', name='accounts_index'),
    url(r'^confirm_email/(\w)+/$', 'confirm_email', name='accounts_confirm_email'),
    url(r'^change_email/$', 'change_email', name='accounts_change_email'),
    url(r'^change_password/$', 'change_password', name='accounts_change_password'),

    url(r'^login/$', 'login', name='login'),
    url(r'^save/$', 'save_character', name='save_character'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^logout-login/$', 'logout', {'login': True}, name='logout-login'),

)
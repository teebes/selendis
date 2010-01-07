from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('stark.apps.accounts.views',
    url(r'^$', 'view_account', name='accounts_index'),
    url(r'^change_email/$', 'change_email', name='accounts_change_email'),
    url(r'^change_password/$', 'change_password', name='accounts_change_password'),
)
from django.conf.urls.defaults import *

from views import openid_login, openid_complete

urlpatterns = patterns('',
    (r'^login/$', openid_login, {}, 'openid-login'),
    (r'^complete/', openid_complete, {}, 'openid-complete'),
)

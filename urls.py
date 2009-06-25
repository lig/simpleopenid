from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('',
    (r'^login/$', openid_login, {}, 'openid-login'),
    (r'^complete/', openid_complete, {}, 'openid-complete'),
    (r'^js/form.js', openid_form_js, {}, 'openid-form-js'),
)

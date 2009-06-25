from django.conf.urls.defaults import *


urlpatterns = patterns('',
    # openid
    (r'^openid/', include('simpleopenid.urls')),
)

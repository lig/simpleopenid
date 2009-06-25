from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.utils.translation import ugettext as _

from ..auth.backends import COMPLETE

from generic import openid_login as generic_openid_login


def openid_complete(request):
    
    result = authenticate(step=COMPLETE, data=(request.GET,
        request.build_absolute_uri(),), session=request.session)
    
    if isinstance(result, User):
        
        login(request, result)
        request.user.message_set.create(message=_('You are logged in.'))
        return HttpResponseRedirect(request.user.get_absolute_url())
    
    else:
        
        return HttpResponseRedirect(reverse('index'))


def openid_login(request):
    return generic_openid_login(request, 'openid/login.html')

'''
Created on 27.04.2009

@author: lig
'''

from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template

from ..auth.backends import BEGIN

def openid_login(request, template, openid_form_class):
    
    if request.method == 'POST':
        openid_form = openid_form_class(request.POST)
        if openid_form.is_valid():
            op_url = authenticate(step=BEGIN,
                data=openid_form.cleaned_data['openid_url'],
                session=request.session)
            return HttpResponseRedirect(op_url)
    else:
        openid_form = openid_form_class()
    
    return direct_to_template(request, template,
        {'openid_login_form': openid_form,})

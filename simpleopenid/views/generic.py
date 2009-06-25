'''
Created on 27.04.2009

@author: lig
'''

from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template

from ..auth.backends import BEGIN
from ..forms import OpendIDLoginForm

def openid_login(request, template):
    
    if request.method == 'POST':
        opendIDLoginForm = OpendIDLoginForm(request.POST)
        if opendIDLoginForm.is_valid():
            op_url = authenticate(step=BEGIN,
                data=opendIDLoginForm.cleaned_data['openid_url'],
                session=request.session)
            return HttpResponseRedirect(op_url)
    else:
        opendIDLoginForm = OpendIDLoginForm()
    
    return direct_to_template(request, template,
        {'openid_login_form': opendIDLoginForm,})

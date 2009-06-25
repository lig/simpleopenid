'''
Created on 23.04.2009

@author: lig
'''

from openid.consumer import consumer
from openid.extensions import sreg

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from ..models import Identity
from ..store import ModelOpenIDStore

BEGIN = 'begin'
COMPLETE = 'complete'

class String(str): pass        

class OpenIDBackend: 
        
    def authenticate(self, step, data, session):
        """
        Authenticate works in two steps as openid does: 'begin' and 'complete'.
        
        At 'begin' step it takes user identity_url and returns url you must
            redirect user to.
        
        At 'complete' step it takes tuple of request.GET parameters received
            from openid provider and current_url then returns User object if
            identity is valid and assigned to some user else it returns openid
            consumer Response object to allow one make own logic for Fail,
            Cancel or Success status responses.
            
            One should use openid.consumer.consumer module variables CANCEL,
            FAILURE, SETUP_NEEDED and SUCCESS to check response.status.
        
        At all steps authenticate need session or other dict like object to
            store state data.
        """
        self.consumer = consumer.Consumer(session, ModelOpenIDStore())
        
        if step == BEGIN:
            return self.begin(data)
        elif step == COMPLETE:
            return self.complete(*data)
        else:
            return None
    
    def begin(self, identity_url):
        auth_request = self.consumer.begin(identity_url)
        sreg_request = sreg.SRegRequest(required=['nickname'],
            optional=['fullname', 'email'])
        auth_request.addExtension(sreg_request)
        redirect_url = auth_request.redirectURL(realm=self.get_realm(),
            return_to=self.get_return_url())
        
        return String(redirect_url)
    
    def complete(self, query, current_url):
        
        op_response = self.consumer.complete(query, current_url)
        
        if op_response.status == consumer.SUCCESS:
            
            try:
                identity = Identity.objects.get(url=op_response.identity_url)
            
            except Identity.DoesNotExist:
                identity = Identity(url=op_response.identity_url,
                    user=Identity.objects.create_openid_user(op_response))
                identity.save()
            
            return identity.user
        
        else:
            return op_response

    
    def get_realm(self):
        current_site = Site.objects.get_current()
        return 'http://%s' % current_site.domain
    
    def get_return_url(self):
        return self.get_realm() + reverse('openid-complete')
    
    def get_user(self, id):
        return User.objects.get(id=id)

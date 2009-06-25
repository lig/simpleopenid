'''
Created on 23.04.2009

@author: lig
'''

import cPickle
import time
from datetime import datetime, timedelta
from openid.association import Association
from openid.store.interface import OpenIDStore
from openid.store.nonce import SKEW

from django.db.models import F

from models import ModelAssociation, Nonce

class ModelOpenIDStore(OpenIDStore):
    """
    This is the class for the store objects the OpenID library uses. This class
    provides mechanism for Django Model Store. It is a single class that
    provides all of the persistence mechanisms that the OpenID library needs,
    for both servers and consumers.
    """
    
    def storeAssociation(self, server_url, association):
        """
        This method puts a Association object into storage, retrievable by
        server URL and handle.
        
        @param server_url: The URL of the identity server that this
            association is with.  Because of the way the server
            portion of the library uses this interface, don't assume
            there are any limitations on the character set of the
            input string.  In particular, expect to see unescaped
            non-url-safe characters in the server_url field.
        
        @param association: The Association to store.
        
        @return: None
        """
        modelAssociation = ModelAssociation(
            server_url=server_url,
            handle=association.handle,
            secret=cPickle.dumps(association.secret),
            issued=datetime.fromtimestamp(association.issued),
            lifetime=association.lifetime,
            assoc_type=association.assoc_type)
        modelAssociation.save()

    def getAssociation(self, server_url, handle=None):
        """
        This method returns an Association object from storage that matches the
        server URL and, if specified, handle. It returns None if no such
        association is found or if the matching association is expired.
        
        If no handle is specified, the store may return any
        association which matches the server URL.  If multiple
        associations are valid, the recommended return value for this
        method is the one most recently issued.
        
        This method is allowed (and encouraged) to garbage collect
        expired associations when found. This method must not return
        expired associations.
        
        @param server_url: The URL of the identity server to get the
            association for.  Because of the way the server portion of
            the library uses this interface, don't assume there are
            any limitations on the character set of the input string.
            In particular, expect to see unescaped non-url-safe
            characters in the server_url field.
        
        @param handle: This optional parameter is the handle of the
            specific association to get.  If no specific handle is
            provided, any valid association matching the server URL is
            returned.
        
        @return: Association for the given identity server.
        """
        
        """ delete expired associations """
        self.cleanupAssociations()
        
        """ filter associations by server_url """
        associations = ModelAssociation.objects.filter(server_url=server_url)
        
        """ filter by handle if needed """
        if handle is not None:
            associations = associations.filter(handle=handle)
        
        """ count associations and return None if there are no one """
        if associations.count() > 0:
            """ get first by default ordering that is by issued time desc """
            association = associations[0]
        else:
            return None
        
        """ construct and return Association instance """
        return Association(
            handle=association.handle,
            secret=cPickle.loads(str(association.secret)),
            issued=time.mktime(association.issued.timetuple()),
            lifetime=association.lifetime,
            assoc_type=association.assoc_type)

    def removeAssociation(self, server_url, handle):
        """
        This method removes the matching association if it's found,
        and returns whether the association was removed or not.
        
        @param server_url: The URL of the identity server the
            association to remove belongs to.  Because of the way the
            server portion of the library uses this interface, don't
            assume there are any limitations on the character set of
            the input string.  In particular, expect to see unescaped
            non-url-safe characters in the server_url field.
        
        @param handle: This is the handle of the association to
            remove.  If there isn't an association found that matches
            both the given URL and handle, then there was no matching
            handle found.
        
        @return: Returns whether or not the given association existed.
        """
        associations = ModelAssociation.objects.filter(server_url=server_url,
            handle=handle)
        if associations.count() > 0:
            associations.delete()
            return True
        else:
            return False
    
    def useNonce(self, server_url, timestamp, salt):
        """Called when using a nonce.

        This method should return True if the nonce has not been used before,
        and store it for a while to make sure nobody tries to use the same
        value again. If the nonce has already been used or the timestamp is
        not current, return False.
        
        You may use openid.store.nonce.SKEW for your timestamp window.
        
        @param server_url: The URL of the server from which the nonce
            originated.
        
        @param timestamp: The time that the nonce was created (to the nearest
            second), in seconds since January 1 1970 UTC.
        
        @param salt: A random string that makes two nonces from the same server
            issued during the same second unique.
        
        @return: Whether or not the nonce was valid.
        """
                
        """ is timestamp current """
        if abs(timestamp - time.time()) > SKEW:
            return False
        
        """ delete expired nonces """
        self.cleanupNonces()
        
        """ filter to find nonce """
        nonces = Nonce.objects.filter(server_url=server_url,
            timestamp=datetime.fromtimestamp(timestamp), salt=salt)
        
        """ if nonce was successfully saved return that nonce is valid """
        if nonces.count() == 0:
            nonce = Nonce(server_url=server_url,
                timestamp=datetime.fromtimestamp(timestamp), salt=salt)
            nonce.save()
            return True
        else:
            return False
    
    def cleanupNonces(self):
        """Remove expired nonces from the store.
        
        Discards any nonce from storage that is old enough that its timestamp
        would not pass useNonce.
        
        This method is not called in the normal operation of the library. It
        provides a way for store admins to keep their storage from filling up
        with expired data.
        
        @return: the number of nonces expired.
        """
        
        """ calculate time that is old enough """
        expired_time = datetime.now() - timedelta(seconds=SKEW)
        
        """ filter for expired nonces """
        expired_nonces = Nonce.objects.filter(timestamp__lt=expired_time)
        
        """ store expired nonces count """
        expired_nonces_count = expired_nonces.count()
        
        """ delete expired nonces """
        expired_nonces.delete()
        
        """ return stored count """
        return expired_nonces_count

    def cleanupAssociations(self):
        """Remove expired associations from the store.
        
        This method is not called in the normal operation of the library. It
        provides a way for store admins to keep their storage from filling up
        with expired data.
        
        @return: the number of associations expired.
        """
                
        """ filter for expired associations """
        expired_associations = ModelAssociation.objects.filter(
            expired__lt=datetime.now())
        
        """ store expired associations count """
        expired_associations_count = expired_associations.count()
        
        """ delete expired associations """
        expired_associations.delete()
        
        """ return stored count """
        return expired_associations_count

    def cleanup(self):
        """Shortcut for cleanupNonces, cleanupAssociations.

        This method is not called in the normal operation of the library. It
        provides a way for store admins to keep their storage from filling up
        with expired data.
        """
        return self.cleanupNonces(), self.cleanupAssociations()

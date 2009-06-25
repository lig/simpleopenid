from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from managers import IdentityManager


class ModelAssociation(models.Model):
    """
    @author: lig
    """
    
    server_url = models.CharField(_('identity server URL'), max_length=1024)
    handle = models.CharField(_('association handle'), max_length=255)
    secret = models.CharField(_('association secret'), max_length=255)
    issued = models.DateTimeField(_('association issued time'))
    lifetime = models.PositiveIntegerField(_('association lifetime (seconds)'))
    assoc_type = models.CharField(_('association type'), max_length=32)
    expired = models.DateTimeField(_('association expired time'),
        editable=False)
    
    def save(self, *args, **kwargs):
        self.expired = self.issued + timedelta(seconds=self.lifetime)
        super(ModelAssociation, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return u'%s: %s' % (self.issued, self.server_url)
    
    class Meta():
        verbose_name = _('server association')
        verbose_name_plural = _('server associations')
        ordering = ['-issued',]

class Nonce(models.Model):
    """
    @author: lig
    """
    
    server_url = models.CharField(_('identity server URL'), max_length=1024)
    timestamp = models.DateTimeField(_('nonce use time'))
    salt = models.CharField(_('nonce salt'), max_length=1024)
    
    def __unicode__(self):
        return u'%s: %s' % (self.timestamp, self.server_url)
    
    class Meta():
        verbose_name = _('nonce')
        verbose_name_plural = _('nonces')
        ordering = ['-timestamp',]

class Identity(models.Model):
    """
    @author: lig
    """
    
    objects = IdentityManager()
    
    user = models.OneToOneField(User, verbose_name=_('Identity user'))
    url = models.CharField(_('identity url'), max_length=1024, unique=True)
    
    def __unicode__(self):
        return u'%s' % self.url
    
    def get_absolute_url(self):
        return self.user.get_absolute_url()        
    
    class Meta():
        verbose_name = _('identity')
        verbose_name_plural = _('identities')
        ordering = ['url',]


class Provider(models.Model):
    """
    @author: lig
    """
    
    name = models.CharField(_('provider name'), max_length=32, unique=True)
    public_url = models.URLField(_('provider public url'), max_length=255)
    service_url = models.CharField(_('provider service url pattern'),
        max_length=255, blank=True,
        help_text=_('use $username for username insertion'), )
    needs_username = models.BooleanField(_('is service url needs username'),
        default=True)
    num = models.IntegerField(_('provider ordering field'), default=0)
    
    def __unicode__(self):
        return u'%s' % self.name
    
    def get_absolute_url(self):
        return self.public_url        
    
    class Meta():
        verbose_name = _('OpenID provider')
        verbose_name_plural = _('OpenID providers')
        ordering = ['num',]

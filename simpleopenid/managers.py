import time

from django.contrib.auth.models import User
from django.db import models

class IdentityManager(models.Manager):
    
    def create_openid_user(self, openid_response):
        sreg_data = openid_response.getSignedNS(
            'http://openid.net/extensions/sreg/1.1')
        
        username = sreg_data.get('nickname', '') or 'user'
        if User.objects.filter(username=username).count() > 0:
            username += '_%s' % time.time()
        
        user = User.objects.create_user(username=username,
            email=sreg_data.get('email', ''))
        
        user_fullname_splitted = sreg_data.get('fullname', '').split(None, 1)
        if len(user_fullname_splitted) > 0:
            user.first_name = user_fullname_splitted[0]
        if len(user_fullname_splitted) == 2:
            user.last_name = user_fullname_splitted[1]
        
        user.save()
        
        return user

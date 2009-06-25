'''
Created on 27.04.2009

@author: lig
'''

from django.contrib import admin

from models import Identity, ModelAssociation, Nonce

admin.site.register(Identity)
admin.site.register(ModelAssociation)
admin.site.register(Nonce)

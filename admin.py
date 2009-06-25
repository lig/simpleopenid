from django.contrib import admin

from models import Identity, ModelAssociation, Nonce, Provider

admin.site.register((Identity, ModelAssociation, Nonce, Provider,))

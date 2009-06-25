from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from models import Provider


__all__ = ['OpendIDLoginForm', 'PrettyOpendIDLoginForm',]

class OpendIDLoginForm(forms.Form):
    """
    @author: lig
    """
    openid_url = forms.URLField()


class PrettyOpendIDLoginForm(forms.Form):
    """
    @author: lig
    """
    provider = forms.ModelChoiceField(queryset=Provider.objects.all(),
        required=True, label=_('Login as user of the'),
        widget=forms.Select(attrs={'onchange':'openid_handle_provider();'}))
    openid_username = forms.CharField(required=False, label='',
        widget=forms.HiddenInput)
    openid_url = forms.URLField(widget=forms.HiddenInput)
    
    def clean_openid_username(self):
        if (self.provider.needs_username and
                not self.cleaned_data['openid_username']):
            raise forms.ValidationError(_('Enter your OpenID name'))
        else:
            return self.cleaned_data['openid_username']
        
    def clean(self):
        pass
            
    
    class Media:
        js = (reverse('openid-form-js'),)

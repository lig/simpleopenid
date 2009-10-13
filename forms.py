from string import Template

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from models import Provider

__all__ = ['OpendIDLoginForm', 'PrettyOpenIDLoginForm',]


class OpendIDLoginForm(forms.Form):
    """
    @author: lig
    """
    openid_url = forms.URLField()


class PrettyOpenIDLoginForm(forms.Form):
    """
    @author: lig
    """
    provider = forms.ModelChoiceField(queryset=Provider.objects.all(),
        required=True, label=_('Login as user of the'),
        widget=forms.Select(attrs={'onchange':'openid_handle_provider();'}))
    openid_username = forms.CharField(required=False, label='',
        widget=forms.HiddenInput)
    openid_url = forms.URLField(required=False, widget=forms.HiddenInput)
    
    def clean(self):
        
        if not 'provider' in self.cleaned_data:
            raise forms.ValidationError(_('Choose your OpenID provider'))
        
        if (self.cleaned_data['provider'].needs_username and
                not self.cleaned_data['openid_username']):
            raise forms.ValidationError(_('Enter your OpenID name'))
        
        self.cleaned_data['openid_url'] = Template(
            self.cleaned_data['provider'].service_url).safe_substitute(
                username=self.cleaned_data['openid_username'])
        return self.cleaned_data
    
    class Media:
        js = (reverse('openid-form-js'),)

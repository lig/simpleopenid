from django import forms
from django.utils.translation import ugettext_lazy as _

from models import Provider


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
        required=True, label=_('Login as user of the'))
    
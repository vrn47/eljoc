from .models import Items, Fixtures, Teams, Teamsdb, Forecasts, Players, Playerdb
from django import forms
from django.utils.translation import gettext_lazy as _


class ItemsForm(forms.ModelForm):
    class Meta:
        model = Items
#        , Teams, Fixtures
        fields = ['description', 'open', 'close', 'fixtures', 'id']
#, 'localteam', 'awayteam'
#        widgets = {
#           'email': forms.EmailField(attrs={'class': 'form-control', 'placeholder': 'Write your account email'})
#        }

class ForecastsForm(forms.ModelForm):
#    items = forms.ModelChoiceField(queryset=Items.objects.filter(id=1))
    class Meta:
        model = Forecasts
#        fields = '__all__'
        fields = ['f_email', 'fvalue1', 'fvalue2']
#        labels = {
#            'f_email': _('Email:'),
#            'fvalue1': _('Local:'),
#            'fvalue2': _('Visitor:'),
#            'f_itemid  ': _('Id:'),
#        }


class PlayersForm(forms.ModelForm):
    class Meta:
        model = Players
        fields = ['p_email']

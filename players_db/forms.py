#from django.forms import ModelForm
from django import forms
from .models import PlayerDB, Players, Editions
from django import forms


class PlayerDBLogForm(forms.ModelForm):
    class Meta:
        model = PlayerDB
        fields = ['email', 'fname', 'lname']
#        widgets = {
#           'email': forms.EmailField(attrs={'class': 'form-control', 'placeholder': 'Write your account email'})
#        }
                
class PlayerDBInfoForm(forms.ModelForm):
    class Meta:
        model = PlayerDB
        fields = "__all__"
        exclude = ['psw']


class PlayerInfoForm(forms.ModelForm):
    class Meta:
        model = Players
        fields = "__all__"
        exclude = ['ppsw']

class EditionsForm(forms.ModelForm):
    class Meta:
        model = Editions
        fields = "__all__"
        exclude = ['ppsw']
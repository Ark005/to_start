

from django import forms
 
class TestForm(forms.Form):
    фамилия = forms.CharField()
    #age = forms.IntegerField()
    счёт = forms.CharField()
    бик = forms.CharField()
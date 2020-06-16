from django import forms
from django.contrib.auth.models import User

class NewNameForm(forms.Form):
    new_name = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Enter new name', 'class':'form-control'}))

    class Meta:
        model = User
        fields = ('new_name')

class SearchForm(forms.Form):
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'search by username', 'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username')
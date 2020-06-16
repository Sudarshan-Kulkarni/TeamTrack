from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class NewUserForm(UserCreationForm):
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Username'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder':'Email Address'}))
    password1 = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder':'Enter password'}))
    password2 = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder':'Confirm password'}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ExistingUserForm(AuthenticationForm):
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder':'Enter password'}))
    class Meta:
        model = User
        fields = ('username', 'password')
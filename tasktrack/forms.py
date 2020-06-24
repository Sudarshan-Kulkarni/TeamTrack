from django import forms
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Collaborators,Task

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

class NewTaskForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(NewTaskForm, self).__init__(*args, **kwargs)
        self.coll_choices = [(x.user_id_1,x.user_id_1) if x.user_id_1!=user else (x.user_id_2,x.user_id_2) for x in Collaborators.objects.filter(Q(user_id_1=user)|Q(user_id_2=user),status=1)]
        self.fields['task_collaborators'] = forms.MultipleChoiceField(label='Choose collaborators',widget=forms.CheckboxSelectMultiple, choices=self.coll_choices)

    task_name = forms.CharField(label='Task Name', required=True,widget=forms.TextInput(attrs={'placeholder':'Give your task a mnemonic name', 'class':'form-control'}))
    task_description = forms.CharField(label='Task Description', widget=forms.Textarea(attrs={'placeholder':'Describe your task (optional)', 'class':'form-control'}))
    
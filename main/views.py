from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from .forms import NewUserForm, ExistingUserForm 
from .queries import get_user_notifications

import json

def login_view(request):
    login_form = ExistingUserForm()
    register_form = NewUserForm()
    context = {
        'login_form':login_form,
        'register_form':register_form
    }
    return render(request, 'main/login.html', context)

def register_redirect(request):
    if request.method=='POST':
        filled_form = NewUserForm(data=request.POST)
        if filled_form.is_valid():
            # Creating new user and updating the database
            user = filled_form.save()
            username = filled_form.cleaned_data.get('username')
            # messages.success(request, "New Account Created:{}".format(username))
            login(request,user)
            return redirect('tasktrack:homepage')
        else:
            all_errors = json.loads(filled_form.errors.as_json())
            print('all_errors = ',(all_errors))
            for field,error in all_errors.items():
                messages.error(request,field+':'+str(error[0]['message']))
            return redirect('main:login_view')
            

def login_redirect(request):
    if request.method=='POST':
        filled_form = ExistingUserForm(data=request.POST)
        if filled_form.is_valid():
            username = filled_form.cleaned_data.get('username')
            password = filled_form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                notifications = get_user_notifications(user.id)
                request.session['notifications'] = notifications

                return redirect('tasktrack:homepage')
            else:
                all_errors = json.loads(filled_form.errors.as_json()).get('__all__')
                for error in all_errors:
                    messages.error(request,error['message'])
                return redirect('main:login_view')
        else:
            all_errors = json.loads(filled_form.errors.as_json()).get('__all__')
            for error in all_errors:
                messages.error(request,error['message'])
            return redirect('main:login_view')
def logout_user(request):
    logout(request)
    return redirect('main:login_view')



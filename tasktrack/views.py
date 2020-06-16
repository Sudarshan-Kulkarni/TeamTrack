from django.shortcuts import render, redirect
from django.contrib.auth.models  import User
from django.http import HttpResponse
from django.contrib import messages

from .forms import NewNameForm, SearchForm
from .queries import search_for_user_username, send_collaborator_request_db, handle_collaborator_request

def user_homepage(request):
    user = request.user
    if request.session.get('collaborator_request_sent', False):
        messages.success(request, "Collaborator request sent!")
        request.session['collaborator_request_sent'] = False

    context = {
        'username':user.username
    }
    return render(request, 'tasktrack/homepage.html', context)

def user_profile(request):
    user = request.user
    context = {
        'user_details' : {
        'Username':[user.username,'tasktrack:changefirstname'],
        'First Name':[user.first_name,'tasktrack:changefirstname'],
        'Last Name':[user.last_name,'tasktrack:changelastname'],
        'Email':[user.email,'tasktrack:changelastname'],
        },
    }
    return render(request, 'tasktrack/profile.html', context)

def change_first_name(request):
    user = request.user
    if request.method=='POST':
        update_user = User.objects.get(id=user.id)
        filled_form = NewNameForm(data=request.POST)
        if filled_form.is_valid():
            update_first_name = filled_form.cleaned_data.get('new_name')
            update_user.first_name = update_first_name
            update_user.save()
            return redirect('tasktrack:profile')
    
    form = NewNameForm()
    context = {
        'form': form
    }
    return render(request,'tasktrack/changefirstname.html',context)

def change_last_name(request):
    user = request.user
    if request.method=='POST':
        update_user = User.objects.get(id=user.id)
        filled_form = NewNameForm(data=request.POST)
        if filled_form.is_valid():
            update_last_name = filled_form.cleaned_data.get('new_name')
            update_user.last_name= update_last_name
            update_user.save()
            return redirect('tasktrack:profile')

    
    form = NewNameForm()
    context = {
        'form': form
    }
    return render(request,'tasktrack/changelastname.html',context)

def add_collaborator(request):
    user = request.user
    form = SearchForm()
    context = {
        'form':form
    } 

    if request.method=='POST':
        filled_form = SearchForm(data=request.POST)
        if filled_form.is_valid():
            search_username = filled_form.cleaned_data.get('username')
            user_list = search_for_user_username(search_username)
            context['user_list'] = user_list
            return render(request, 'tasktrack/addcollaborator.html', context)

    return render(request, 'tasktrack/addcollaborator.html', context)

def send_collaborator_request(request):
    user = request.user
    if request.method=='POST':
        form_data = request.POST
        request_user_id = form_data.get('request_user_id')
        user_id_1 = user.id

        if send_collaborator_request_db(user_id_1, request_user_id)[0]:
            request.session['collaborator_request_sent'] = True
            return redirect('tasktrack:homepage')
        else:
            return redirect('tasktrack:addcollaborator')

def notifications_view(request):
    user = request.user
    print(request.session.get('notifications'))
    return render(request, 'tasktrack/notifications.html')

def handle_notification(request):
    user = request.user
    if request.method=='POST':
        form_data = request.POST
        '''
        1 - accept
        0 - reject
        '''
        action = 1 if form_data.get('accept_collaborator_request', False) else 0
        action_id = form_data.get('accept_collaborator_request') if action==1 else form_data.get('reject_collaborator_request')
        handle_collaborator_request(user.id, action_id, action)
        request.session['notifications'] = list(filter(lambda x: int(x['id'])!=int(action_id), request.session['notifications']))
    return redirect('tasktrack:homepage')
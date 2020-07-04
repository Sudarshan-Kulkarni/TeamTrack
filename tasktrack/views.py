from django.shortcuts import render, redirect
from django.contrib.auth.models  import User
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test

from .forms import NewNameForm, SearchForm, NewTaskForm
from .queries import search_for_user_username, send_collaborator_request_db, handle_collaborator_request, get_all_collaborators, write_new_task, get_all_user_tasks, get_task_details, check_user_is_member_of_task


def is_user_member_of_task(user,task_id):
    return check_user_is_member_of_task(user, task_id)


@login_required
def user_homepage(request):
    user = request.user

    tasks = get_all_user_tasks(user)

    if request.session.get('collaborator_request_sent', False):
        messages.success(request, "Collaborator request sent!")
        request.session['collaborator_request_sent'] = False

    context = {
        'username':user.username,
        'tasks':tasks
    }
    return render(request, 'tasktrack/homepage.html', context)

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
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
@login_required
def notifications_view(request):
    user = request.user
    print(request.session.get('notifications'))
    return render(request, 'tasktrack/notifications.html')

@login_required
def handle_notification(request):
    user = request.user
    if request.method=='POST':
        form_data = request.POST
        '''
        Actions -
        1 - accept
        0 - reject
        '''
        action = 1 if form_data.get('accept_collaborator_request', False) else 0
        action_id = form_data.get('accept_collaborator_request') if action==1 else form_data.get('reject_collaborator_request')
        handle_collaborator_request(user.id, action_id, action)
        request.session['notifications'] = list(filter(lambda x: int(x['id'])!=int(action_id), request.session['notifications']))
    return redirect('tasktrack:homepage')

@login_required
def collaborators_view(request):
    user = request.user
    collaborator_list = get_all_collaborators(user.id)
    context = {
        'username': user.username,
        'collaborator_list':collaborator_list
    }
    return render(request, 'tasktrack/collaborators.html', context)

@login_required
def create_new_task(request):
    user = request.user
    if request.method=='POST':
        filled_form = NewTaskForm(user, data=request.POST)
        if filled_form.is_valid():
            filled_form = filled_form.cleaned_data
            task_name = filled_form['task_name']
            task_description = filled_form['task_description']
            task_collaborators = filled_form['task_collaborators']

            write_new_task(task_name, task_description, user, task_collaborators)
            print(task_name,task_description,task_collaborators)
            return redirect('tasktrack:createnewtask')

    form = NewTaskForm(user)
    context = {
        'user': user.username,
        'form': form
    }
    return render(request, 'tasktrack/createnewtask.html', context)

@login_required
def tasks(request, task_id=None):
    if task_id is not None:
        if is_user_member_of_task(request.user,task_id):
            task_details = get_task_details(task_id)  
            context = {
                'task_details':task_details
            }
            return render(request, 'tasktrack/taskdetails.html', context)
        else:
            return HttpResponse("not authorized")
    else:
        return redirect('main:login')
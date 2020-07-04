from django.contrib.auth.models import User
from django.db.models import Q

from main.queries import get_username_from_userid

from .models import Collaborators, Task


def search_for_user_username(username):
    username = username.lower()
    users = User.objects.filter(username__icontains=username)
    return users

def send_collaborator_request_db(user_id_1, user_id_2):
    try:
        (user_id_1,user_id_2) = (int(user_id_1),int(user_id_2))
        user_1 = User.objects.get(id=min(user_id_1,user_id_2))
        user_2 = User.objects.get(id=max(user_id_1,user_id_2))

        if user_1.id == user_id_1:
            tmp_user = user_1
        else:
            tmp_user = user_2

        col_req = Collaborators(user_id_1=user_1, user_id_2=user_2, status=0, action_user_id=tmp_user)
        col_req.save()
        return (True,None)
    except Exception as E:
        print(E)
        return (False,E)

def handle_collaborator_request(user_id, action_id, action):
    collaborator_request = Collaborators.objects.get(id=action_id)
    collaborator_request.action_user_id = User.objects.get(id=user_id)

    if action:        
        collaborator_request.status = 1 
    else:
        collaborator_request.status = 2

    collaborator_request.save()
    return True

def get_all_collaborators(user_id):
    current_user = User.objects.get(id=user_id)
    raw_collaborators = list(Collaborators.objects.filter(Q(user_id_1=current_user)|Q(user_id_2=current_user),status=1).values())

    collaborators = []
    username_cache = {}

    for coll in raw_collaborators:
        tmp = {}
        tmp['id'] = coll['id']
        other_user_id = list(filter(lambda x: int(x)!=int(user_id) , [coll.get('user_id_1_id'),coll.get('user_id_2_id')]))[0]
        if other_user_id not in username_cache.keys():
            other_username = get_username_from_userid(other_user_id)
        else:
            other_username = username_cache[other_user_id]
        
        tmp['user_id'] = other_user_id
        tmp['username'] = other_username
        collaborators.append(tmp)
    return collaborators

def write_new_task(task_name, task_description, user, task_collaborators):
    new_task = Task(task_name=task_name, task_description=task_description)
    new_task.save()

    new_task.users.add(user)
    for u in task_collaborators:
        new_task.users.add(User.objects.get(username__icontains=u.lower()))

def get_all_user_tasks(user):
    tasks = list(Task.objects.filter(users=user).values())
    return tasks

def check_user_is_member_of_task(user, task_id):
    task = Task.objects.get(id=task_id)
    return user in task.users.all()

def get_task_details(task_id):
    task_details = Task.objects.get(id=task_id)
    return task_details
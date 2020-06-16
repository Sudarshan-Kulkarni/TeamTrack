from .models import Collaborators
from django.contrib.auth.models  import User



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



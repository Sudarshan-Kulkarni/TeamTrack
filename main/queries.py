from django.contrib.auth.models import User
from django.db.models import Q

from tasktrack.models import Collaborators

def get_username_from_userid(user_id):
    return User.objects.get(id=user_id).username

def get_user_notifications(user_id):
    current_user = User.objects.get(id=user_id)
    raw_notifications = Collaborators.objects.filter(Q(user_id_1=current_user)|Q(user_id_2=current_user),  ~Q(action_user_id=current_user),status=0).values()
    raw_notifications = list(raw_notifications)
    username_cache = {}
    notifications = []
    
    for notif in raw_notifications:
        tmp = {}
        tmp['id'] = notif['id']
        other_user_id = list(filter(lambda x: int(x)!=int(user_id) , [notif.get('user_id_1_id'),notif.get('user_id_2_id')]))[0]
        if other_user_id not in username_cache.keys():
            other_username = get_username_from_userid(other_user_id)
        else:
            other_username = username_cache[other_user_id]
            
        tmp['username'] = other_username
        notifications.append(tmp)
    return notifications


from django.db import models

from django.contrib.auth.models import User

class Collaborators(models.Model):
    '''
    The status field represents whether the friendship is pending or already decided.
    0 - pending
    1 - accepted
    2 - declined
    3 - blocked

    The action_user_id represents the person who took the latest action.
    '''

    user_id_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_user_1')
    user_id_2 = models.ForeignKey(User, on_delete=models.CASCADE,related_name='%(class)s_user_2')
    status = models.IntegerField()
    action_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_action_user')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id_1','user_id_2'], name='unique_friendship')
        ]
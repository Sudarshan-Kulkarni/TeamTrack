from django.urls import path
from . import views

app_name = "tasktrack"

urlpatterns = [
    path('',views.user_homepage, name='homepage'),
    path('homepage/', views.user_homepage, name='homepage'),
    path('profile/', views.user_profile, name='profile'),
    path('changefirstname/', views.change_first_name, name='changefirstname'),
    path('changelastname/', views.change_last_name, name='changelastname'),
    path('addcollaborator/', views.add_collaborator, name='addcollaborator'),
    path('send_collaborator_request/', views.send_collaborator_request, name='send_collaborator_request'),
    path('notifications/',views.notifications_view, name='notifications'),
    path('handle_notification/',views.handle_notification, name='handle_notification')
]
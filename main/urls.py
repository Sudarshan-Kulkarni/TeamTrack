from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('login/',views.login_view, name='login_view'),
    path('register_redirect/', views.register_redirect, name='register_redirect'),
    path('login_redirect/', views.login_redirect, name='login_redirect'),
    path('logout/', views.logout_user, name='logout')
]
from django.urls import path, re_path


import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('register/', authapp.register, name='register'),
    path('profile/', authapp.profile, name='profile'),
    path('logout/', authapp.logout, name='logout'),
    re_path(r'^verify/(?P<email>.+)/(?P<activation_key>\w+)/$', authapp.verify, name='verify')
]
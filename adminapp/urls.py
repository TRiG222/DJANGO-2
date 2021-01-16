from django.urls import path

import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.index, name='index'),
    path('users/', adminapp.UsersListView.as_view(), name='admin_users'),
    path('users/create/', adminapp.UsersCreateView.as_view(), name='admin_users_create'),
    path('users/update/<int:pk>/', adminapp.UsersUpdateView.as_view(), name='admin_users_update'),
    path('users/remove/<int:pk>/', adminapp.UserDeleteView.as_view(), name='admin_users_remove'),
]
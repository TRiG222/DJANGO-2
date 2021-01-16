from django.urls import path

import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    path('add/<int:id>/', basketapp.basket_add, name='basket_add'),
    path('remove/<int:id>/', basketapp.basket_remove, name='basket_remove'),
    path('edit/<int:id>/<int:quantity>/', basketapp.basket_edit, name='basket_edit'),
    ]
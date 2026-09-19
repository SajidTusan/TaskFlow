from django.urls import path
from . import views


urlpatterns = [

path(
    '',
    views.TaskListView.as_view(),
    name='home'
),

    path(
        'create/',
        views.create_task,
        name='create_task'
    ),

    path(
        'delete/<int:id>/',
        views.delete_task,
        name='delete_task'
    ),

    path(
        'toggle/<int:id>/',
        views.toggle_task,
        name='toggle_task'
    ),

    path(
        'register/',
        views.register,
        name='register'
    ),
]
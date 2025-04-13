from django.urls import path
from taskapp.views.generic_views import *
from taskapp.views.task_views import *

urlpatterns = [

    # task endpoints
    path('tasks/', manage_tasks, name='manage_tasks'),
    path('tasks/<int:id>/', manage_tasks, name='manage_tasks'),

    # profile endpoints
    path('profiles/', manage_profiles, name='manage_profiles'),
    path('profiles/<int:id>/', manage_profiles, name='manage_profiles'),

    # subtask endpoints
    path('subtasks/', manage_subtasks, name='manage_subtasks'),
    path('subtasks/<int:id>/', manage_subtasks, name='manage_subtasks'),

    # category endpoints
    path('categories/', manage_categories, name='manage_categories'),
    path('categories/<int:id>/', manage_categories, name='manage_categories'),

    # tag endpoints
    path('tags/', manage_tags, name='manage_tags'),
    path('tags/<int:id>/', manage_tags, name='manage_tags'),

    # user endpoints
    path('users/', manage_users, name='manage_users'),
    path('users/<int:id>/', manage_users, name='manage_users'),

    # overdue tasks
    path('overdue_tasks/', overdue_tasks, name='overdue_tasks'),
]
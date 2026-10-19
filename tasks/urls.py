from django.urls import path
from . import views
app_name = 'tasks'
urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/new/', views.task_new, name='task_new'),
    path('tasks/<int:task_id>/edit/', views.task_edit, name='task_edit'),
    path('tasks/<int:task_id>/delete/', views.task_delete, name='task_delete'),
    path('tasks/<int:task_id>/toggle/', views.task_toggle, name='task_toggle'),
]

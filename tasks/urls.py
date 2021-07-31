from django.urls import path
from . import views

urlpatterns = [
    path("",views.TasksListView.as_view() , name="tasks"),
    path("toggle-check/<int:id>/",views.toggle_check , name="toggle-check"),
    path("update-task/<int:pk>/",views.TaskUpdateView.as_view() , name="update-task"),
    path("delete-task/<int:pk>/",views.TaskDeleteView.as_view() , name="delete-task"),
    path("create-task/",views.TaskCreateView.as_view() , name="create-task"),
]
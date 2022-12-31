from django.urls import path
from tasks.views import TasksAPIView, TaskDetailAPIView

urlpatterns = [
    path('', TasksAPIView.as_view(), name='tasks'),
    path('<int:id>', TaskDetailAPIView.as_view(), name='task'),
]

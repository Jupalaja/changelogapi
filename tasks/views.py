from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from tasks.serializers import TaskSerializer
from tasks.models import Task
import authentication.jwt


class TasksAPIView(ListCreateAPIView):
    authentication_classes = (authentication.jwt.JWTAuthentication,)
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter)

    filterset_fields = ['id', 'title', 'desc', 'is_completed', 'created_at', 'creator']
    search_fields = ['id', 'title', 'desc', 'is_completed', 'created_at']

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        return Task.objects.all()


class TaskDetailAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = (authentication.jwt.JWTAuthentication,)
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        return Task.objects.all()

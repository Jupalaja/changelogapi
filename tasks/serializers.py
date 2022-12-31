from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from tasks.models import Task
from authentication.models import User


class TaskSerializer(ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Task
        fields = ('title', 'desc', 'is_completed', 'created_at', 'creator',)

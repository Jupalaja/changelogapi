from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from tasks.models import Task
from authentication.models import User


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'desc', 'is_completed', 'created_at', 'creator_id',)
        read_only_fields = ['creator_id']

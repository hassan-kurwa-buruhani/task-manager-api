from taskapp.models.subtask import SubTask
from rest_framework import serializers
from .task_serializers import TaskSerializer

class SubTaskSerializer(serializers.ModelSerializer):
    main_task = serializers.SlugRelatedField(
        read_only=True, slug_field='title', queryset=Task.objects.all())

    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'main_task', 'status']
        read_only_fields = ['id', 'main_task']
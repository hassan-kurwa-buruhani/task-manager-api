from taskapp.models.task import Task
from taskapp.models.tag import Tag
from .tag_serializers import  TagSerializer
from rest_framework import serializers
from .category_serializers import CategorySerializer


class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), source='tags', write_only=True
    )

    is_completed = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    progress = serializers.ReadOnlyField()

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'category',
            'category_id',
            'user',
            'due_date',
            'priority',
            'recurrence',
            'status',
            'tags',
            'tag_ids',
            'is_completed',
            'is_overdue',
            'progress',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

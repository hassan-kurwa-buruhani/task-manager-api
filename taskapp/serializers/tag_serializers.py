from taskapp.models.tag import Tag
from taskapp.models.user import CustomUser
from rest_framework import serializers
from .user_serializers import UserSerializer

class TagSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username', read_only=True, queryset=CustomUser.objects.all())


    class Meta:
        model = Tag 
        fields = ['id', 'name', 'user']
        read_only_fields = ['id', 'user']
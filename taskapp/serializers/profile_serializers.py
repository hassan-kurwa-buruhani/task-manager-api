from taskapp.models.profile import Profile
from .user_serializers import UserSerializer
from rest_framework import serializers

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'age', 'gender', 'profile_pic']
        read_only_fields = ['id', 'user']
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from taskapp.models.task import Task
from taskapp.serializers.task_serializers import TaskSerializer
from taskapp.models.profile import Profile
from taskapp.serializers.profile_serializers import ProfileSerializer
from taskapp.models.subtask import SubTask
from taskapp.serializers.subtask_serializers import SubTaskSerializer
from taskapp.models.category import Category
from taskapp.serializers.category_serializers import CategorySerializer
from taskapp.models.tag import Tag
from taskapp.serializers.tag_serializers import TagSerializer
from taskapp.models.user import CustomUser
from taskapp.serializers.user_serializers import UserSerializer



def generic_api(model_class, serializer_class):

    """
    A generic api view for all models for simple and basic CRUD operations
    """

    @api_view(['GET', 'POST', 'DELETE', 'PUT']) 

    
    def api(request, id=None):
        if request.method == 'GET':
            if id:
                try:
                    instance =model_class.objects.get(id=id)
                    serializer = serializer_class(instance)
                    return Response(serializer.data)
                except model_class.DoesNotExist:
                    return Response({'message': 'Object not found'})
            else:
                instance = model_class.objects.all()
                serializer = serializer_class(instance, many=True)
                return Response(serializer.data)
        elif request.method == 'POST':
            serializer = serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            user = request.user
            if id:
                try:
                    instance =model_class.objects.get(id=id)
                    serializer = serializer_class(instance, data=request.data)
                    if serializer.is_valid():
                        serializer.save(lecturer=user)
                        
                    return Response(serializer.data)
                except model_class.DoesNotExist:
                    return Response({'message': 'Object not found'})
                
        elif request.method == 'DELETE':
            if id:
                try:
                    instance = model_class.objects.get(id=id)
                    instance.delete()
                    return Response({'message': 'Deleted successfully'})
                except model_class.DoesNotExist:
                    return Response({'message': 'Object not found'})
    return api

manage_tasks = generic_api(Task, TaskSerializer)
manage_profiles = generic_api(Profile, ProfileSerializer)
manage_subtasks = generic_api(SubTask, SubTaskSerializer)
manage_categories = generic_api(Category, CategorySerializer)
manage_tags = generic_api(Tag, TagSerializer)
manage_users = generic_api(CustomUser, UserSerializer)

from taskapp.models.task import Task, Status
from django.shortcuts import render
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from taskapp.serializers.task_serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated



# Create your views here.

# overdue tasks
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def overdue_tasks(request):
    """
    Returns a list of overdue tasks for the authenticated user.
    """
    user = request.user
    overdue_tasks = Task.objects.filter(user=user).overdue()

    if not overdue_tasks.exists():
        return Response({'message': 'You have no overdue tasks'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(overdue_tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



# tasks overdue today
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def overdue_today(request):

    """
        Fetches all tasks that are overdue today for the authenticated user
    """

    user = request.user
    today = timezone.now().date()
    tasks_overdue_today = Task.objects.filter(due_date__date=today, user=user).overdue()

    if not tasks_overdue_today.exists():
        return Response({'message': 'You have no overdue tasks today'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(tasks_overdue_today, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# weekly summary view
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weekly_summary(request):

    """
        Fetches the weekly summary for completed, in progress and overdue tasks
    """

    user = request.user
    
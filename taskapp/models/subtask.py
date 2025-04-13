from django.db import models
from .base import BaseModel
from .task import Task, Status

class SubTask(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    main_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    status = models.CharField(max_length=255, choices=Status.choices)


    def __str__(self):
        return f"{self.title} (Subtask of {self.main_task.title})"

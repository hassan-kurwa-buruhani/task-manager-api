from django.db import models
from django.utils import timezone
from .base import BaseModel
from .user import CustomUser
from .category import Category
from .tag import Tag

class Priority(models.TextChoices):
    LOW = 'Low', 'Low'
    MEDIUM = 'Medium', 'Medium'
    HIGH = 'High', 'High'

class Status(models.TextChoices):
    IN_PROGRESS = 'In Progress', 'In Progress'
    COMPLETED = 'Completed', 'Completed'
    CANCELLED = 'Cancelled', 'Cancelled'
    OVERDUE = 'Overdue', 'Overdue'
    ON_DEADLINE = 'On Deadline', 'On Deadline'

class Task(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='tasks')
    due_date = models.DateTimeField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tasks')
    priority = models.CharField(max_length=255, choices=Priority.choices)
    status = models.CharField(max_length=255, choices=Status.choices)
    tags = models.ManyToManyField(Tag, related_name='tasks', blank=True)

    @property
    def is_overdue(self):
        return self.due_date < timezone.now() and self.status not in [Status.COMPLETED, Status.CANCELLED]

    def __str__(self):
        return f"{self.title} by {self.user.username}"

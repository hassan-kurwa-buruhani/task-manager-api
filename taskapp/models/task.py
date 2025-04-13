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

class Recurrence(models.TextChoices):
    NONE = 'None', 'None'
    DAILY = 'Daily', 'Daily'
    WEEKLY = 'Weekly', 'Weekly'
    MONTHLY = 'Monthly', 'Monthly'
    YEARLY = 'Yearly', 'Yearly'

class TaskQuerySet(models.QuerySet):
    def overdue(self):
        return self.filter(due_date__lt=timezone.now()).exclude(status=Status.COMPLETED)

    def in_progress(self):
        return self.filter(status=Status.IN_PROGRESS)

class Task(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='tasks')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tasks')
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=Priority.choices)
    recurrence = models.CharField(max_length=10, choices=Recurrence.choices, default=Recurrence.DAILY)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.IN_PROGRESS)
    tags = models.ManyToManyField(Tag, blank=True, related_name='tasks')

    objects = TaskQuerySet.as_manager()

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=["user", "status"]),
        ]

    @property
    def is_completed(self):
        return self.status == Status.COMPLETED

    @property
    def is_overdue(self):
        return self.due_date < timezone.now() and self.status not in [Status.COMPLETED, Status.CANCELLED]

    @property
    def progress(self):
        total = self.subtasks.count()
        if total == 0:
            return 0
        completed = self.subtasks.filter(status=Status.COMPLETED).count()
        return round((completed / total) * 100, 2)

    def __str__(self):
        return f"{self.title} by {self.user.username}"

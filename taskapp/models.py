from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


# Priority choices
class Priority(models.TextChoices):
    LOW = 'Low', _('Low')
    MEDIUM = 'Medium', _('Medium')
    HIGH = 'High', _('High')


# Status choices
class Status(models.TextChoices):
    IN_PROGRESS = 'In Progress', _('In Progress')
    COMPLETED = 'Completed', _('Completed')
    CANCELLED = 'Cancelled', _('Cancelled')
    OVERDUE = 'Overdue', _('Overdue')
    ON_DEADLINE = 'On Deadline', _('On Deadline')


# Recurrence choices
class Recurrence(models.TextChoices):
    NONE = 'None', _('None')
    DAILY = 'Daily', _('Daily')
    WEEKLY = 'Weekly', _('Weekly')
    MONTHLY = 'Monthly', _('Monthly')


# Custom user model
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# Abstract base model
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Profile model
class Profile(BaseModel):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


# Category model
class Category(BaseModel):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


# Tag model
class Tag(BaseModel):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('name', 'user')
        ordering = ['name']

    def __str__(self):
        return self.name


# Task model
class Task(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, default=None, on_delete=models.SET_NULL, null=True, blank=True)
    due_date = models.DateTimeField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tasks')
    priority = models.CharField(max_length=255, choices=Priority.choices)
    status = models.CharField(max_length=255, choices=Status.choices)
    recurrence = models.CharField(max_length=20, choices=Recurrence.choices, default=Recurrence.NONE)
    tags = models.ManyToManyField(Tag, blank=True, related_name='tasks')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=["user", "status"]),
        ]

    def __str__(self):
        return f"{self.title} created by {self.user.username}"

    @property
    def is_completed(self):
        return self.status == Status.COMPLETED

    @property
    def is_overdue(self):
        return self.due_date and self.due_date < timezone.now()

    @property
    def progress(self):
        total = self.subtasks.count()
        completed = self.subtasks.filter(status=Status.COMPLETED).count()
        return int((completed / total) * 100) if total else 0


# SubTask model
class SubTask(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    main_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    status = models.CharField(max_length=255, choices=Status.choices)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} for task: {self.main_task.title}"

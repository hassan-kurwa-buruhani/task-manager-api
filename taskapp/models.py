from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

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

# Custom user model
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

# Base model
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

    def __str__(self):
        return self.name


# Task model
class Task(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, default="Uncategorized", on_delete=models.CASCADE)
    due_date = models.DateTimeField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    priority = models.CharField(max_length=255, choices=Priority.choices)
    status = models.CharField(max_length=255, choices=Status.choices)  

    def __str__(self):
        return f"{self.title} created by {self.user.username}"


# SubTask model
class SubTask(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    main_task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=Status.choices)

    def __str__(self):      
        return f"{self.title} created by {self.main_task.user.username}"





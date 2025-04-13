from django.db import models
from .base import BaseModel
from .user import CustomUser

class Tag(BaseModel):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tags', default=None)

    class Meta:
        unique_together = ('name', 'user')
        ordering = ['name']

    def __str__(self):
        return self.name

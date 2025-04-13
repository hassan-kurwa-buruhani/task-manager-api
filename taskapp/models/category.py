from django.db import models
from .base import BaseModel

class Category(BaseModel):
    name = models.CharField(max_length=255)

    class Meta: 
        ordering = ['name']
        verbose_name_plural = 'categories'
        verbose_name = 'category'

    def __str__(self):
        return self.name

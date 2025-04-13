from django.db import models
from .base import BaseModel

class Tag(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

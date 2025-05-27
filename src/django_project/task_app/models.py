import uuid

from django.db import models
from django.forms import CharField

class Task(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(
        'user_app.User', related_name='tasks'
    )

    class Meta:
        db_table = "Task"
        app_label = "task_app"

    def __str__(self):
        return self.name
    
    

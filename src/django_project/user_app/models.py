import uuid

from django.db import models

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username
    
    @property
    def is_authenticated(self):
        """Check if the user is authenticated."""
        return True

    class Meta:
        db_table = 'user'
        app_label = 'user_app'
        
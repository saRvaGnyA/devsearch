import uuid
from django.db import models

# Create your models here.


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, editable=False, unique=True)
    demo_link = models.TextField(null=True, blank=True, max_length=2000)
    source_link = models.TextField(null=True, blank=True, max_length=2000)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

from tkinter import CASCADE
import uuid
from django.db import models
from sqlalchemy import null

# Create your models here.


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, editable=False, unique=True)
    featured_image = models.ImageField(
        null=True, blank=True, default="default.jpg")
    demo_link = models.TextField(null=True, blank=True, max_length=2000)
    source_link = models.TextField(null=True, blank=True, max_length=2000)
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField("Tag", blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self) -> str:
        return self.title


class Review(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    VOTE_TYPE = (('up', 'Up Vote'), ('down', 'Down Vote'))
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, unique=True, editable=False)
    body = models.TextField(max_length=2000, null=True, blank=True)

    def __str__(self) -> str:
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, unique=True, editable=False)

    def __str__(self) -> str:
        return self.name

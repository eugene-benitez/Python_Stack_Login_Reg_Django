from __future__ import unicode_literals
from django.db import models

# Create your models here.


class JobManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['job']) < 3:
            errors["title"] = "Title should be at least 2 characters"
        if len(postData['description']) < 10:
            errors["description"] = "Description should be at least 10 characters"
        if len(postData['location']) < 1:
            errors["location"] = "Location must not be blank"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Jobs(models.Model):
    job = models.CharField(max_length=255)
    location = models.TextField()
    description = models.TextField()
    user_posted = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name="jobs")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = JobManager()

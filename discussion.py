from __future__ import unicode_literals
from django.db import models


class Job(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.Textfield()
    creator = models.ForeignKey(User, related_name="job_created")
    acceptor = models.ForeignKey(User, related_name="job_accepted", null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    # job = models.ForeignKey(Job, related_name="job_users")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

from django.db import models

from django.contrib.auth.models import User, UserManager
from django.contrib import admin
from django.utils import timezone
# Create your models here.

from django.db import models


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=40)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)

    def __str__(self):
        return self.user.username


class Group(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    members = models.ManyToManyField(Person, through='Membership')
    genre = models.CharField(max_length=100)
    description = models.TextField(max_length=500, default='No description yet')
    pic = models.ImageField(upload_to="hw/",  null=True, blank=True, max_length=1000)

    def __str__(self):
        return self.name


class Membership(models.Model):
    person = models.ForeignKey(Person)
    group = models.ForeignKey(Group)
    date_joined = models.DateField()

    def __str__(self):
        return str(self.person)+" in "+str(self.group)

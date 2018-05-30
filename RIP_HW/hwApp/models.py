from django.db import models

from django.contrib.auth.models import User

from django.utils import timezone
from django.db import models


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.user.username


class Group(models.Model):
    user = models.ForeignKey('Person')
    name = models.CharField(max_length=128, blank=False, null=False)

    genre = models.ManyToManyField('Genre')
    description = models.TextField(max_length=500, default='No description yet')
    pic = models.ImageField(upload_to="hw/", null=True, blank=True, max_length=1000)
    rating = models.IntegerField(default=0)
    pub_date = models.DateTimeField(default=timezone.now)

    def counter(self):
        self.rating = int((Like.objects.filter(group=self, rate=True).count() - Like.objects.filter(
            group=self, rate=False).count()))

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey('Person')
    group = models.ForeignKey('Group')
    text = models.TextField()
    rating = models.IntegerField(default=0)
    popular = models.BooleanField(default=False)
    pub_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return "{} {}".format(self.group.name, self.pub_date)


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return "{}".format(self.name)

    def __str__(self):
        return self.name


class Like(models.Model):
    group = models.ForeignKey(Group)
    like_author = models.ForeignKey(User)
    rate = models.BooleanField(default=None)

    class Meta:
        unique_together = ['group', 'like_author']

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import CASCADE
from django.urls import reverse


class ChatUser(User):
    nickname = models.CharField(null=False, max_length=100, default='alice')


class Room(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(null=False, max_length=500, default='Chat Room')

    def get_absolute_url(self):
        return reverse('room', args=[self.slug])


class Message(models.Model):
    message = models.TextField(null=False, blank=False)
    room = models.ForeignKey(Room, on_delete=CASCADE)
    author = models.ForeignKey(ChatUser, on_delete=CASCADE)

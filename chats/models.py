from django.db import models
from django.contrib.auth.models import User
from accounts.models import Picture



class FriendRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_request')
    friend = models.ManyToManyField(User, related_name='user_friend_request')


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend')
    friend = models.ManyToManyField(User, related_name='user_friend')


class SentRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_request')
    friend = models.ManyToManyField(User, related_name='user_sent_request')


class ChatThread(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outbox')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inbox')
    date = models.DateTimeField(auto_now_add=True)


class ChatMessage(models.Model):
    text = models.TextField()
    thread = models.ForeignKey(ChatThread, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


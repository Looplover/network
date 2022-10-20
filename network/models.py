from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    sender = models.ForeignKey("User", on_delete=models.PROTECT, related_name="emails_sent")
    subject = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField()

class Comment(models.Model):
    commenter = models.ForeignKey("User", on_delete=models.CASCADE, related_name="comment")
    post = models.ForeignKey("Post", on_delete=models.PROTECT, related_name="comments")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Follow(models.Model):
    follower = models.ForeignKey("User", on_delete=models.PROTECT, related_name="followings")
    following = models.ForeignKey("User", on_delete=models.PROTECT, related_name="followers")


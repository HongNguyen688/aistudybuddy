from django.db import models
from django.contrib.auth.models import User

class ChatTopic(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ChatContent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(ChatTopic, on_delete=models.CASCADE, related_name="allmessages")
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.user.username}: {self.message} at {self.timestamp.strftime("%b %d,%Y, %H:%M:%S")}"

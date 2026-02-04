from django.db import models
from django.contrib.auth.models import User

class CardTopic(models.Model):
  name = models.CharField(max_length=200)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return self.name
  
class FlashCard(models.Model):
  question = models.TextField()
  answer = models.TextField()
  topic = models.ForeignKey(CardTopic, on_delete=models.CASCADE, related_name="flashcards")
  timestamp = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.question[:68] #first 68 chars

class PDFDocument(models.Model):
  topic = models.ForeignKey(CardTopic, on_delete=models.CASCADE, related_name="pdfs")
  file = models.FileField(upload_to="documents/")
  uploaded_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f" PDF for {self.topic.name} uploaded on {self.uploaded_at.strftime(' %b %d,%Y, %H:%M:%S')}"
from django.db import models
from django.contrib.auth.models import User

class QuizTopic(models.Model):
  name = models.CharField(max_length=200)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name
  
class QuizContent(models.Model):
  question = models.TextField()
  answer1 = models.CharField(max_length=255)
  answer2 = models.CharField(max_length=255)
  answer3 = models.CharField(max_length=255)
  answer4 = models.CharField(max_length=255)

  CHOICEIDX = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
  ]
  correct_answer = models.PositiveSmallIntegerField(choices=CHOICEIDX)
  order = models.PositiveIntegerField(default=1)

  topic = models.ForeignKey(QuizTopic, on_delete=models.CASCADE, related_name='allquestions')
  timestamp = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.question[:120]


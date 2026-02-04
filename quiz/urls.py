from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('quiz', views.quizzes, name='quiz'),
  path('takequiz', views.takequizzes, name='takequiz'),
]
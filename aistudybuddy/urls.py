from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import render

def homepage(request):
  return render(request, "index.html")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("chat/", include("chat.urls")),
    path("notes/", include("notes.urls")),
    path("flashcards/", include("flashcards.urls")),
    path("quiz/", include("quiz.urls")),
    path("",homepage, name="index"),
   
]

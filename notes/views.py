from django.shortcuts import render

# Create your views here.
def index(request):
  return render(request, 'index.html')

def notes(request):
  return render(request, 'Notes/notes.html')
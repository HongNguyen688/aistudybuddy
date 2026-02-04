from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse

# Create your views here.
def index(request):
  return render(request, 'index.html')

def user_login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user_login = authenticate(request, username=username, password=password)

    if user_login is not None:
      login(request, user_login)
      return HttpResponseRedirect(reverse('index'))
    else:
      return render(request, 'Accounts/login.html',{
        "message": "Invalid username or password."
      })

  else:
    return render(request, 'Accounts/login.html')

def user_logout(request):
  logout(request)
  return HttpResponseRedirect(reverse('index'))

def user_register(request):
  if request.method =='POST':
    username = request.POST['username']
    email = request.POST['email']
    password =  request.POST['password']
    confirmpassword = request.POST['confirmpassword']

    if password != confirmpassword:
      return render(request, 'Accounts/register.html', {
        "message": "Passwords do not match."
      })
    elif User.objects.filter(username=username).exists():
      return render(request, 'Accounts/register.html', {
        "message": "Username already taken. Let's create a new one."
      })
    else:
      user = User.objects.create_user(username=username, email=email, password=password)
      user.save()
      login(request, user)
      return HttpResponseRedirect(reverse('index'))

  return render(request, 'Accounts/register.html')
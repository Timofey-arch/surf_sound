from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import PlaylistUser


def index(request):
    return HttpResponse("It is SurfSound, YO")


def signup(request):
    context= {'username':True,'email':True}
    if not request.user.is_anonymous:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if (username,) in User.objects.values_list("username",):
            context['username'] = False
            return render(request,'signup.html',context)

        elif (email,) in User.objects.values_list("email",):
            context['email'] = False
            return render(request,'signup.html',context)

        PlaylistUser.objects.create(username=username)
        new_user = User.objects.create_user(username, email, password)
        new_user.save()
        login(request,new_user)
        return redirect('/')
    return render(request,'signup.html',context)
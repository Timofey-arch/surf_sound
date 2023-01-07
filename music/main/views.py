from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import playlist_user
from youtube_search import YoutubeSearch


def index(request):
    if request.user.is_anonymous:
        return redirect('/login')
    if request.method == 'POST':
        pass
    # Изменена стандардтная страничка после входа
    return render(request, 'playlist.html')


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

        playlist_user.objects.create(username=username)
        new_user = User.objects.create_user(username,email,password)
        new_user.save()
        login(request,new_user)
        return redirect('/')
    return render(request,'signup.html',context)


def login_auth(request):
    if not request.user.is_anonymous:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            context = {'case':False}
            return render(request, 'login.html', context)
    context = {'case':True}
    return render(request, 'login.html', context)


def logout_auth(request):
    logout(request)
    return redirect('/login')


def playlist(request):
    if request.user.is_anonymous:
        return redirect('/login')

    cur_user = playlist_user.objects.get(username = request.user)

    try:
      song = request.GET.get('song')
      song = cur_user.playlist_song_set.get(song_title=song)
      song.delete()
    except:
      pass

    if request.method == 'POST':
        add_playlist(request)
        return HttpResponse("")
    # song = 'kSFJGEHDCrQ'
    user_playlist = cur_user.playlist_song_set.all()
    return render(request, 'playlist.html', {'song':song,'user_playlist':user_playlist})


def add_playlist(request):
    cur_user = playlist_user.objects.get(username = request.user)

    if (request.POST['title'],) not in cur_user.playlist_song_set.values_list('song_title', ):

        songdic = (YoutubeSearch(request.POST['title'], max_results=1).to_dict())[0]
        song__albumsrc=songdic['thumbnails'][0]
        cur_user.playlist_song_set.create(song_title=request.POST['title'],song_dur=request.POST['duration'],
        song_albumsrc = song__albumsrc,
        song_channel=request.POST['channel'], song_date_added=request.POST['date'],song_youtube_id=request.POST['songid'])


def search(request):
    if request.method == 'POST':
        add_playlist(request)
        return HttpResponse("")
    try:
        search = request.GET.get('search')
        song = YoutubeSearch(search, max_results=10).to_dict()
        song_li = [song[:10:2],song[1:10:2]]
    except:
        return redirect('/')

    return render(request, 'search.html', {'CONTAINER': song_li, 'song':song_li[0][0]['id']})

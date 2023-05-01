from django.middleware.csrf import get_token
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from .models.room import Room
from room.game.main import Game


@login_required
def launch_room(request):
    room = Room.objects.create(hoster=request.user)
    Game.initialize(room.pk)
    return JsonResponse({'room number': room.code})


def index(request):
    return HttpResponse('index')


def get_csrf(request):
    if request.method == 'GET':
        return JsonResponse({'csrftoken':get_token(request),'sessionid': request.COOKIES.get('sessionid')})
    

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'csrftoken':get_token(request),'sessionid': request.COOKIES.get('sessionid')})

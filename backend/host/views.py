from threading import Thread
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponse
from .models.host import Host
from room.game.main import Game
from room.models.broadcast import Player



@login_required
def launch_room(request):
    room = Host.objects.create(hoster=request.user)
    Game.initialize(room.pk)
    return JsonResponse({'room number': room.room_code})


def index(request):
    return HttpResponse('index')
    
@csrf_exempt
def get_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'user_id': request.user.id})
        else:
            return HttpResponse('not authenticate')

@csrf_exempt
def create_room(request):
    if request.method == 'POST':
        room_name = request.POST['room_name']
        if  Host.objects.filter(room_name=room_name):
            return HttpResponse('room name exist')
        room = Host.objects.create(hoster=request.user, room_name=room_name)
        room.open_room()
        room.save()
        return HttpResponse(room.room_code)

@csrf_exempt
def join_room(request):
    if request.method == 'POST':
        room_code = request.POST['room_code']
        room = Host.objects.get(room_code=room_code)
        room.players.add(request.user)
        Player.objects.create(user=request.user)
        return JsonResponse({'players': [x.username for x in room.players.all()]})

@csrf_exempt
def check_player(request):
    if request.method == 'POST':
        room_code = request.POST['room_code']
        room = Host.objects.get(room_code=room_code)
        return JsonResponse({'players': [x.username for x in room.players.all()]})
    
@csrf_exempt
def start_game(request):
       if request.method == 'POST':
        room_name = request.POST['room_name']
        Host.objects.get(pk=room_name).room_name='Init'.save()
        game = Game.factory(room_name)
        # create a thread
        thread = Thread(target=game.start)
        # run the thread
        thread.start()
        return HttpResponse('game start')

@csrf_exempt
def check_room_status(request):
    if request.method == 'POST':
        room_name = request.POST['room_name']
        room = Host.objects.get(pk=room_name)
        return HttpResponse(room.room_status)
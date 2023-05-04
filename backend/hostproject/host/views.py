from threading import Thread
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from .models import Host


def index(request):
    return HttpResponse('index')


@csrf_exempt
def create_room(request):
    if request.method == 'POST':
        room_name = request.POST['room_name']
        user = User.objects.get(pk=request.POST['user_id'])
        if  Host.objects.filter(room_name=room_name):
            return HttpResponse('room name exist')
        room = Host.objects.create(hoster=user, room_name=room_name)
        room.save()
        return HttpResponse(room.room_name)

@csrf_exempt
def join_room(request):
    if request.method == 'POST':
        room_code = request.POST['room_code']
        user_id = request.POST['user_id']
        room = Host.objects.get(room_code=room_code)
        room.players.add(User.objects.get(pk=user_id))
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
        # game = Game.factory(room_name)
        # # create a thread
        # thread = Thread(target=game.start)
        # thread.start()
        return HttpResponse('game start')

@csrf_exempt
def check_room_status(request):
    if request.method == 'POST':
        room_name = request.POST['room_name']
        room = Host.objects.get(room_name=room_name)
        return HttpResponse(room.room_status)
    
# allow user find those joining room names 
@csrf_exempt
def get_user_room_pk(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        user = User.objects.get(pk=user_id)
        return HttpResponse([x for x in user.host_set.all()])
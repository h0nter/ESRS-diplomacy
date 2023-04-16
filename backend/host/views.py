from django.contrib.auth.decorators import login_required
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
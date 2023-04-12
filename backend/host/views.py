from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models.room import Room
from room.game.main import Game


@login_required
def launch_room(request):
    room = Room.objects.create(hoster=request.user)
    Game.initialize(room.pk)
    return JsonResponse({'room number': room.code})

def join(request):
    room_code:str
    pass

# initial room
def launch():
    pass

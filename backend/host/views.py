from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Room
from room.models.order import Turn
from room.game.main import Game


# @login_required
def launch_room(request):
    turn = Turn.objects.create(year=1901)
    user = request.user
    room = Room.objects.create(turn=turn, hoster=user)
    room.save()
    room.player.add(user)
    Game.initialize(room.pk)
    return HttpResponse({'room number': room.pk})

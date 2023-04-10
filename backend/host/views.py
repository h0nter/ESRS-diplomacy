from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Room
from room.models.order import Turn
from room.game.main import Game


# @login_required
def launch_room(request):
    user = request.user
    turn = Turn.objects.create(year=1901)
    room = Room.objects.create(hoster=user, turn=turn)
    room.save()
    room.player.add(user)
    Game.initialize(room.pk)
    return HttpResponse({'room number': room.pk})

def invitations(request):
    # if request.method == 'POST':
    #     form = CustomUserCreationForm(request.POST)
    #     if form.is_valid():
    #         user = form.save()
    #         # Authenticate and log in the user
    #         username = form.cleaned_data.get('username')
    #         password = form.cleaned_data.get('password1')
    #         user = authenticate(request, username=username, password=password)
    #         login(request, user)
    #         return redirect('/')
    # else:
    #     form = CustomUserCreationForm()
    # return render(request, 'host/register.html', {'form': form})
    pass
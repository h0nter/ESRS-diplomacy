from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from host.models import Host


@api_view()
def hello_world(request):
    return Response({"message": "Hello, world!"})

    
@api_view(["POST"])
def start_game(request):
    #    if request.method == 'POST':
        room = Host.objects.get(pk=request.POST.get("room_id"))
        # room = Host.objects.get(pk=2)
        room.room_name = 'Init'
        room.save()
        print(room.room_status)
        return Response(room.room_status)
        # game = Game.factory(room_name)
        # # create a thread
        # thread = Thread(target=game.start)
        # thread.start()
        # return Response('game start')

    
@api_view(['POST'])
def get_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'user_id': request.user.id})
        else:
            return Response('not authenticated')
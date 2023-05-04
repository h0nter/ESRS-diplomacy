from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from host.models import Host


@api_view()
def hello_world(request):
    return Response({"message": "Hello, world!"})

@api_view(['POST'])
def create_room(request):
    if request.method == 'POST':
        room_name = request.POST['room_name']
        user_id = request.POST['user_id']
        if  Host.objects.filter(room_name=room_name):
            return Response('room name exist')
        room = Host.objects.create(hoster=User.objects.get(pk=user_id), room_name=room_name)
        room.create()
        return Response(room.room_name)

@api_view(['POST'])
def join_room(request):
    if request.method == 'POST':
        room_code = request.POST['room_code']
        user_id = request.POST['user_id']
        room = Host.objects.get(room_code=room_code)
        room.players.add(User.objects.get(pk=user_id))
        return Response({'players': [x.username for x in room.players.all()]})

@api_view(['POST'])
def check_player(request):
    if request.method == 'POST':
        room_code = request.POST['room_code']
        room = Host.objects.get(room_code=room_code)
        return Response({'players': [x.username for x in room.players.all()]})
    
@api_view(['POST'])
def start_game(request):
       if request.method == 'POST':
        room_name = request.POST['room_name']
        Host.objects.get(pk=room_name).room_name='Init'.save()
        # game = Game.factory(room_name)
        # # create a thread
        # thread = Thread(target=game.start)
        # thread.start()
        return Response('game start')

@api_view(['POST'])
def check_room_status(request):
    if request.method == 'POST':
        room_name = request.POST['room_name']
        room = Host.objects.get(room_name=room_name)
        return Response(room.room_status)
    
# allow user find those joining room names 
@api_view(['POST'])
def get_user_room_pk(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        user = User.objects.get(pk=user_id)
        return Response([x for x in user.host_set.all()])
    
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
            return Response('not authenticate')
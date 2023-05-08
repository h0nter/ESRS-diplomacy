from django.contrib.auth import login, authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from host.models import Host, RoomStatus, UserRoom
from .speaker import add_player, add_room

@api_view()
def hello_world(request):
    return Response({"message": "Hello, world!"})


@api_view(["POST"])
def start_game(request):
    if request.method == 'POST':
        room = Host.objects.get(pk=request.POST.get("room_id"))
        room.status = RoomStatus.INITIALIZE
        response_data = add_room(port=room.port, room_name=room.room_name)
        room.room_id = response_data['data']['createRoom']['room']['id']
        room.save()
        
        for user in UserRoom.objects.filter(room=room):
            add_player(port=room.port, user_id=user.user.pk, room_id=room.pk)
        
        return Response(response_data)

    
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
from django.contrib.auth import login, authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from host.models import Host, RoomStatus, UserHost
from .speaker import add_player, add_room, initialize

@api_view()
def hello_world(request):
    return Response({"message": "Hello, world!"})


@api_view(["POST"])
def start_game(request):
    if request.method == 'POST':
        host = Host.objects.get(pk=request.POST.get("host_id")) # need to communicate with frount-end, change room_id to host_id
        host.status = RoomStatus.INITIALIZE
        response_data = add_room(port=host.port, room_name=host.room_name)
        host.room_id = response_data['data']['createRoom']['room']['id']
        host.save()
        
        for user in UserHost.objects.filter(host=host):
            add_player(port=host.port, user_id=user.user.pk, room_id=host.room_id)
        
        initialize(port=host.port, room_id=host.room_id)

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
        

@api_view(['POST'])
def player_list(request):
    if request.method == 'POST':
        host_id = request.POST['host_id']
        res = []
        for user_host in UserHost.objects.filter(host__id=host_id):
            res.append({
                "user_id": user_host.user.pk,
                "username": user_host.user.get_username()
            })
        
        return Response(res)
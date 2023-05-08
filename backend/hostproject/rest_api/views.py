import requests
from django.contrib.auth import login, authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from host.models import Host, RoomStatus

@api_view()
def hello_world(request):
    return Response({"message": "Hello, world!"})


def game_triger(port, room_name) -> int:
    url = "http://127.0.0.1:"+str(port)+"/graphql"
    query_template = '''
    mutation{
        createRoom(roomName:" %s "){
            room{
                id,
                roomName
            }
        }
    }
    '''
    query = query_template % room_name
    headers = { 'Content-Type': 'application/json' }
    data = {'query': query}

    return requests.post(url, headers=headers, json=data).json()


@api_view(["POST"])
def start_game(request):
    #    if request.method == 'POST':
        room = Host.objects.get(pk=request.POST.get("room_id"))
        # room = Host.objects.get(pk=2)
        room.room_name = RoomStatus.WAITING
        room.save()
        response_data=game_triger(room.port, room.room_name)
        room.room_id = response_data['data']['createRoom']['room']['id']
        room.save()

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
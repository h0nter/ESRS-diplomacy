from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from .models import Host


def index(request):
    return HttpResponse('index')


@csrf_exempt
def join_room(request):
    if request.method == 'POST':
        room_code = request.POST['room_code']
        user_id = request.POST['user_id']
        room = Host.objects.get(room_code=room_code)
        room.players.add(User.objects.get(pk=user_id))
        return JsonResponse({'players': [x.username for x in room.players.all()]})

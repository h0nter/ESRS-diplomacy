from django.http import HttpResponse
from django.http import Http404
import secrets
from models import User


# Create your views here.
def insex(request):
    return HttpResponse('index page')

def register(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        try:
            user = User.objects.get(name=name)
            return HttpResponse('user already exist')
        except User.DoesNotExist:
            token = secrets.token_hex(16)
            user = User(name=name, cookies = token)
            user.save()
            return HttpResponse('here is your cookies').set_cookie('cookie_name', token)
    else:
        return  Http404("wrong api method")
    

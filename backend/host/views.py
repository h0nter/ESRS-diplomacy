# from django.http import HttpResponse
# from django.http import HttpResponseNotAllowed
# from django.views.decorators.csrf import csrf_exempt
# import secrets
# from .models import User


# # Create your views here.
# def index(request):
#     return HttpResponse('index page')

# @csrf_exempt
# def register(request):
#     if request.method == 'POST':
#         name = request.POST.get("name")
#         try:
#             user = User.objects.get(name=name)
#             return HttpResponse('user already exist')
#         except User.DoesNotExist:
#             token = secrets.token_hex(16)
#             user = User(name=name, cookies = token)
#             user.save()
#             return HttpResponse('here is your cookies').set_cookie('cookie_name', token)
#     else:
#         return  HttpResponseNotAllowed(['POST'])
    

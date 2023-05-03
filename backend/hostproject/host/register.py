from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
import json


def registration(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Authenticate and log in the user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            # return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'host/register.html', {'form': form})


# csrf token response
def my_view(request):
    if request.method == 'POST':
        return JsonResponse({'csrfmiddlewaretoken': get_token(request)})


@csrf_exempt
def get_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'user_id': request.user.id})
        else:
            return HttpResponse('not authenticate')
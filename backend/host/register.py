from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from django.middleware.csrf import get_token
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

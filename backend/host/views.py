from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm


# Create your views here.
def index(request):
    return HttpResponse('index page')


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
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'host/register.html', {'form': form})

# useing django build-in function to authenticate user
def something_else(request):
    if request.user.is_authenticated:
        # Do something for authenticated users.
        ...
    else:
        # Do something for anonymous users.
        ...
    
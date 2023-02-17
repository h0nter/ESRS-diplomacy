from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
# import json


# Create your views here.
def index(request):
    return HttpResponse("index page")
    
def map(request):
    graph = {
            "a" : ["b", "c"],
            "b" : ["a", "d"],
            "c" : ["a"],
            "d" : ["b"]
            }
    return JsonResponse(graph)


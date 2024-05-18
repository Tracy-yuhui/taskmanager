# /home/taskmanager/api/views.py

from django.http import HttpResponse

def api_home(request):
    return HttpResponse("Welcome to the API home!")


from django.shortcuts import render

# Create your views here.

def index(request):
    map_loc = []
    context = {
        'map_loc': map_loc
    }
    return render(request, 'test/index.html', context)
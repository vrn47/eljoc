from django.shortcuts import render
from .models import Players

# Create your views here.

def casa(request):
    players = Players.objects.all()
    context = {
        'players': players
    }
    return render(request, 'casa.html', context)
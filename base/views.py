from django.shortcuts import render
from .models import Room
from .forms import RoomForm

def home(request):
    rooms = Room.objects.all()
    return render(request, 'base/home.html', {"rooms": rooms})

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {"room": room}

    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        print(request.POST)
    context = {"form": form}
    return render(request, 'base/room_form.html', context)
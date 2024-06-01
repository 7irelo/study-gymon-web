from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import Room, Subject
from .forms import RoomForm

def loginPage(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "incorrect password")
        except:
            messages.error(request, "Incorrect username")

        
    context = {"page": page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect("home")

def registerPage(request):
    page = "register"
    context = {"page": page}
    return render(request, 'base/login_register.html', context)

def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    rooms = Room.objects.filter(Q(subject__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    
    subjects = Subject.objects.all()
    room_count = rooms.count()

    context = {"rooms": rooms, "subjects": subjects, "room_count": room_count}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {"room": room}

    return render(request, 'base/room.html', context)

@login_required(login_url="login")
def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url="login")
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url="login")
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect("home")

    return render(request, 'base/delete.html', {"obj": room})
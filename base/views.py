from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import Room, Subject, Message
from .forms import RoomForm

def loginPage(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username").lower()
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
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occured during registration")
    context = {"form": form}
    return render(request, 'base/login_register.html', context)

def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    rooms = Room.objects.filter(Q(subject__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    
    subjects = Subject.objects.all()
    room_count = rooms.count()
    messages = Message.objects.filter(Q(room__subject__name__icontains=q))

    context = {"rooms": rooms, "subjects": subjects, "room_count": room_count, "comments": messages}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    messages = room.message_set.all().order_by("created")
    participants = room.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get("body")
        )
        room.participants.add(request.user)
        return redirect("room", pk=room.id)
    context = {"room": room, "comments": messages, "participants": participants}
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    messages = user.message_set.all()
    subjects = Subject.objects.all()
    context = {"user": user, "rooms": rooms, "subjects":subjects, "comments": messages}
    return render(request, 'base/profile.html', context)

@login_required(login_url="login")
def createRoom(request):
    form = RoomForm()
    subjects = Subject.objects.all()
    
    if request.method == "POST":
            subject_name = request.POST.get("subject")
            subject, created = Subject.objects.get_or_create(name=subject_name)

            Room.objects.create(
                host=request.user,
                subject=subject,
                name=request.POST.get("name"),
                description=request.POST.get("description")
            )
        
        #form = RoomForm(request.POST)
        #if form.is_valid():
            #room = form.save(commit=False)
            #room.host = request.user
            #room.save()
            return redirect("home")
    context = {"form": form, "subjects": subjects}
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

@login_required(login_url="login")
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.method == "POST":
        message.delete()
        return redirect("home")

    return render(request, 'base/delete.html', {"obj": message})
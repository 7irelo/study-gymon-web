from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import Room, Subject, Message, Topic, User
from .forms import RoomForm, UserForm, MyUserCreationForm

def loginPage(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
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
    form = MyUserCreationForm()
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
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
    
    subjects = Subject.objects.all()[0:10]
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
    topics = Topic.objects.all()
    
    if request.method == "POST":
            subject_name = request.POST.get("subject")
            topic_name = request.POST.get("topic")
            subject, created = Subject.objects.get_or_create(name=subject_name)
            topic, created = Topic.objects.get_or_create(name=topic_name)

            Room.objects.create(
                host=request.user,
                subject=subject,
                topic=topic,
                name=request.POST.get("name"),
                description=request.POST.get("description")
            )
        
        #form = RoomForm(request.POST)
        #if form.is_valid():
            #room = form.save(commit=False)
            #room.host = request.user
            #room.save()
            return redirect("home")
    context = {"form": form, "subjects": subjects, "topics": topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url="login")
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.method == "POST":
        subject_name = request.POST.get("subject")
        topic_name = request.POST.get("topic")
        subject, created = Subject.objects.get_or_create(name=subject_name)
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get("name")
        room.subject = subject
        room.topic = topic
        room.description = request.POST.get("description")
        room.save()
        
        return redirect("home")
    context = {"form": form, "topics": topics, "room": room}
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

@login_required(login_url="login")
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid:
            form.save()
            return redirect("user-profile", pk=user.id)
    context = {"form": form}
    return render(request, "base/update_user.html", context)

def subjectsPage(request):
    subjects = Subject.objects.all()
    

    context = {"subjects": subjects}
    return render(request, "base/subjects.html", context)
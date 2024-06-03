from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from base.models import Room
from django.core.serializers import serialize

def getRoutes(request):

    data = [
        'GET /api/rooms',
        'GET /api/rooms/:id',
        'GET /api/subjects',
    ]
    return JsonResponse(data, safe=False)

def getRooms(request):
    rooms = Room.objects.all()
    data = list(rooms.values())
    return JsonResponse(data, safe=False)

def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    data = {
        "id": room.id,
        "host_id": "room.host",
        "subject_id": room.subject,
        "topic_id": room.topic,
        "name": room.name,
        "description": room.description,
        "updated": room.updated,
        "created": room.created
    }
    return JsonResponse(data, safe=False)
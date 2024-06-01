from django.contrib import admin

from .models import Subject, Room, Message


admin.site.register(Subject)
admin.site.register(Room)
admin.site.register(Message)
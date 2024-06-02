from django.contrib import admin

from .models import Subject, Topic, Room, Message


admin.site.register(Subject)
admin.site.register(Topic)
admin.site.register(Room)
admin.site.register(Message)
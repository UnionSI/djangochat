from django.contrib import admin

from .models import Room, Message

@admin.register(Room)
class AdminRoom(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Message)
class AdminMessage(admin.ModelAdmin):
    list_display = ('room', 'user', 'content', 'date_added')
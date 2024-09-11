from django.contrib import admin
from .models import Slot, Comment


# Register your models here.

@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'end_time', 'context', 'cost', 'status', 'specialist')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'reason', 'client', 'text', 'slot')

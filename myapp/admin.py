from django.contrib import admin
from .models import Task,Room,Message
# Register your models here.

admin.site.register(Task)
admin.site.register(Room)
admin.site.register(Message)
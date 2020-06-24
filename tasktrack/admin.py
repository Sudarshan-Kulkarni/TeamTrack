from django.contrib import admin
from .models import Collaborators, Task, SubTask

# Register your models here.
admin.site.register(Collaborators)
admin.site.register(Task)
admin.site.register(SubTask)
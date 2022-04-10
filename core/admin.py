from django.contrib import admin
from .models import Tree, Species, Origin, Task, Tasklist

admin.site.register(Tree)
admin.site.register(Species)
admin.site.register(Origin)
admin.site.register(Tasklist)
admin.site.register(Task)

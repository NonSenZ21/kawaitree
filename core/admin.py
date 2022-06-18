from django.contrib import admin
from .models import Tree, Species, Origin, Task, Tasklist, Photo, Linkcat, Link

admin.site.register(Tree)
admin.site.register(Species)
admin.site.register(Origin)
admin.site.register(Tasklist)
admin.site.register(Task)
admin.site.register(Photo)
admin.site.register(Linkcat)
admin.site.register(Link)

# class PhotoAdmin(admin.ModelAdmin):
#     def thumb(self, object):
#         try:
#             return True
#         except:
#             pass

# admin.site.register(Photo, PhotoAdmin)

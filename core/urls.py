from django.urls import path
from . import views
urlpatterns = [
   path('',views.tdb, name='core-tdb'),
   path('about/',views.about, name='core-about'),

]
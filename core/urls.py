from django.urls import path
from .views import TreeListView, TreeDetailView, TreeCreateView, TreeUpdateView, TreeDeleteView
from . import views
urlpatterns = [
   path('',views.tdb, name='core-tdb'),
   path('list/',TreeListView.as_view(), name='list'),
   path('tree/<int:pk>/',TreeDetailView.as_view(), name='tree-detail'),
   path('tree/new/',TreeCreateView.as_view(), name='tree-create'),
   path('tree/<int:pk>/update/', TreeUpdateView.as_view(), name='tree-update'),
   path('tree/<int:pk>/delete/', TreeDeleteView.as_view(), name='tree-delete'),
   path('about/',views.about, name='core-about'),

]
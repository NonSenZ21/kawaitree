from django.urls import path
from .views import TreeListView, TreeCreateView, TreeUpdateView, TreeDeleteView, \
   TaskDeleteView, PhotoDetailView, PhotoDeleteView
from . import views
urlpatterns = [
   path('', views.tdb, name='core-tdb'),
   path('list/',TreeListView.as_view(), name='list'),
   path('tree/<int:pk>/', views.treedetail, name='tree-detail'),
   path('tree/new/', TreeCreateView.as_view(), name='tree-create'),
   path('tree/<int:pk>/update/', TreeUpdateView.as_view(), name='tree-update'),
   path('tree/<int:pk>/delete/', TreeDeleteView.as_view(), name='tree-delete'),
   path('task/<int:pk>/', views.taskdetail, name='task-detail'),
   path('task/new/<int:treepk>/', views.taskcreate, name='task-create'),
   path('task/update/<int:pk>/', views.taskupdate, name='task-update'),
   path('task/delete/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),
   path('photo/<int:pk>/', PhotoDetailView.as_view(), name='photo-detail'),
   path('photo/new/<int:tree>/<int:task>/', views.photocreate, name='photo-create'),
   # path('photo/<int:pk>/update/', PhotoUpdateView.as_view(), name='photo-update'),
   path('photo/<int:pk>/delete/', PhotoDeleteView.as_view(), name='photo-delete'),
   path('about/', views.about, name='core-about'),
]

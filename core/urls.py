from django.urls import path
from .views import TreeListView, TreeDetailView, TreeCreateView, TreeUpdateView, TreeDeleteView, TaskDetailView, TaskDeleteView
from . import views
urlpatterns = [
   path('',views.tdb, name='core-tdb'),
   path('list/',TreeListView.as_view(), name='list'),
   path('tree/<int:pk>/', TreeDetailView.as_view(), name='tree-detail'),
   path('tree/new/', TreeCreateView.as_view(), name='tree-create'),
   # path('tree/<int:pk>/update/', TreeUpdateForm(), name='tree-update'),
   path('tree/<int:pk>/update/', TreeUpdateView.as_view(), name='tree-update'),
   path('tree/<int:pk>/delete/', TreeDeleteView.as_view(), name='tree-delete'),
   path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
   path('task/new/<int:treepk>/', views.TaskCreate, name='task-create'),
   path('task/update/<int:pk>/', views.TaskUpdate, name='task-update'),
   path('task/delete/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),
   path('photo/new/', views.PhotoCreate, name='photo-create'),
   path('about/', views.about, name='core-about'),

]
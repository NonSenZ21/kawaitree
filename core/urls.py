from django.urls import path
from .views import TreeListView, TreeCreateView, TreeUpdateView, TreeDeleteView, \
   TaskDeleteView, PhotoDetailView, PhotoDeleteView, LinksView, FaqView
from . import views
urlpatterns = [
   path('', views.tdb, name='core-tdb'),
   path('list/', TreeListView.as_view(), name='list'),
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
   path('photo/list/<int:owner>/', views.photolist, name='photo-list'),
   path('photo/listall/<int:owner>/<int:species>/', views.photolistall, name='photo-listall'),
   path('photo/<int:pk>/delete/', PhotoDeleteView.as_view(), name='photo-delete'),
   path('tasks/<int:action>/', views.tasks, name='core-tasks'),
   path('members_map/', views.membersmap, name='members_map'),
   path('faq/', FaqView.as_view(), name='faq'),
   path('links/', LinksView.as_view(), name='links'),
]

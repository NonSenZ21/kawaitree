from django.urls import path
from .views import UserDeleteView
from . import views
urlpatterns = [
   path('', views.profile, name='profile'),
   path('<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
   path('weather/', views.weather, name='weather'),
   path('public_profile/<int:pk>/', views.pubprofile, name='public_profile'),
]

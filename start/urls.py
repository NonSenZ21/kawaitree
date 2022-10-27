from django.urls import path
from django.views.generic import TemplateView

from . import views
urlpatterns = [
   path('', views.home),
   path('sw.js', views.service_worker),
   path('offline/', TemplateView.as_view(template_name="start/offline.html")),
]
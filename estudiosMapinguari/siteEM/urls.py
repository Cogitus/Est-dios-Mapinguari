from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload, name='inicial'),
    path('analisar/', views.analisar, name='analisar'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload, name='inicial'),
    path('analise/', views.analisar, name='analise')
]
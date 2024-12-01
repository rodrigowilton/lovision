from django.urls import path
from .views import ImagemView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('imagem/', ImagemView.as_view(), name='imagem-view'),
]

from django.urls import path, include
from . import views

urlpatterns = [

    # url стартовой страницы
    path('', views.load_diagn, name='diagnostic'),
    path('photo-diagnostic/', views.photo_diagnostic,
         name='photo_diagnostic'),
]
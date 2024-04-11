from django.urls import path , include
from . import views


urlpatterns = [

    path('', views.load_result,
         name='result'),

    path('list-result-type-photo/', views.load_type_result_photo,
         name='result_type'),

    path('result-photo/', views.load_type_result_photo,
         name='result_photo'),

]

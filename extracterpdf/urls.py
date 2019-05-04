from django.urls import path
from extracterpdf import views


app_name = 'extracterpdf'

urlpatterns = [

    path('', views.index, name='index'),


    ]

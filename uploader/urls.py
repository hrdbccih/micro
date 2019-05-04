from django.urls import path
from . import views


app_name = 'uploader'

urlpatterns = [

    path('index/', views.index, name='index'),

    path('consolider/', views.consolider, name='consolider_nav'),

    path('consolider/<int:pk>', views.consolider, name='consolider'),

    path('confirmer/<int:pk>', views.confirmer, name='confirmer'),

    path('read/', views.read, name='read'),

    path('confirmado/<int:pk>', views.confirmado, name = 'confirmado'),

    path('deleter/', views.deleter, name='deleter_nav'),

    path('deletado/<int:pk>', views.deletado, name='deletado'),

    path('consolidafiles', views.consolidafiles, name='consolidafiles')


    ]

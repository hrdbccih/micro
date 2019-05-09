from django.conf.urls import url
from . import views

app_name = 'biao'

urlpatterns = [

    url(r'^$', views.hrdb, name='hrdb'),

    #url(r'^register/$', views.register, name='register'),

    url(r'^login_user/$', views.login_user, name='login_user'),

    url(r'^logout_user/$', views.logout_user, name='logout_user'),

    url(r'^index/$', views.index, name='index'),

    url(r'^(?P<pk>[0-9]+)/$', views.detail, name='detail'),

    url(r'^param/(?P<param>.+)$', views.index_filtered, name='index_filtered'),

    url(r'^agente/(?P<agente>.+)$', views.agente, name='agente'),

    url(r'^relacao/(?P<agente>.+)$', views.relacao, name='relacao'),

    url(r'^mdrs/$', views.mdrs, name='mdrs'),

    url(r'^read/$', views.read, name='read'),

    url(r'^limpahospital/$', views.limpahopsital, name='limpahospital'),

    ]

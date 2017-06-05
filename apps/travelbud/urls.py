from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^travels$', views.travels, name='travels'),
    url(r'^add$', views.add_travel_plan, name='add'),
    url(r'^newTravelPlan$', views.newTravelPlan, name='newTravelPlan'),
    url(r'^destination/(?P<id>\d+)*$', views.destination, name='destination'),
    url(r'^join/(?P<id>\d+)*$', views.join, name='join'),


]

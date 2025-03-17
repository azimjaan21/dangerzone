from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('save_polygons/', views.save_polygons, name='save_polygons'),
    path('get_polygons/', views.get_polygons, name='get_polygons'),

]

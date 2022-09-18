from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    path('', views.all_rooms, name='all_rooms'),
    url(r'token$', views.token, name="token"),
    path('rooms/<str:slug>/', views.room_detail, name="room_detail"),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chat/<int:chat_id>/', views.chat_room, name='chat_room'),
]

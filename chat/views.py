from django.shortcuts import render, get_object_or_404
from .models import Chat

def index(request):
    return render(request, 'chat/index.html')

def chat_room(request, chat_id):
    chat = get_object_or_404(Chat, pk=chat_id)
    return render(request, 'chat/chat_room.html', {'chat': chat})

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Chat, Message
from django.contrib.auth.models import User

# Define una clase que hereda de AsyncWebsocketConsumer para manejar WebSockets de manera asíncrona
class ChatConsumer(AsyncWebsocketConsumer):
    
    # Método que se llama cuando un cliente intenta conectarse al WebSocket
    async def connect(self):
        # Obtiene el ID del chat desde los argumentos de la URL en el scope
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        # Define el nombre del grupo del chat basado en el ID del chat
        self.chat_group_name = f'chat_{self.chat_id}'

        # Agrega el canal actual al grupo del chat
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        # Acepta la conexión WebSocket
        await self.accept()

    # Método que se llama cuando un cliente se desconecta del WebSocket
    async def disconnect(self, close_code):
        # Elimina el canal actual del grupo del chat
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    # Método que se llama cuando se recibe un mensaje a través del WebSocket
    async def receive(self, text_data):
        # Convierte el texto recibido a un diccionario de Python
        data = json.loads(text_data)
        message = data['message']
        user = self.scope['user']  # Obtiene el usuario actual del scope

        # Guarda el mensaje en la base de datos de manera asíncrona
        chat = await sync_to_async(Chat.objects.get)(pk=self.chat_id)
        # Puedes descomentar la siguiente línea si también deseas guardar el mensaje en la base de datos
        # await sync_to_async(Message.objects.create)(chat=chat, sender=user, content=message)

        # Envía el mensaje al grupo del chat
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',  # Tipo de evento a manejar
                'message': message,
                'sender': user.username,
            }
        )

    # Método que maneja el evento 'chat_message' para enviar el mensaje a través del WebSocket
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Envía el mensaje al cliente WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))


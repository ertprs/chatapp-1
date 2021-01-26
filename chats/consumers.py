import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer

from .models import ChatThread, ChatMessage


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.thread_id = self.scope['url_route']['kwargs']['id']
        self.thread = ChatThread.objects.get(id=self.thread_id)
        self.friend_thread = ChatThread.objects.get(user=self.thread.friend, friend=self.thread.user)
        user = self.thread.user
        friend = self.thread.friend
        self.room_group_name = 'chat'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )


    # Receive message from Websocket
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']


        ChatMessage.objects.create(thread=self.thread, user=self.thread.user, text=message)
        ChatMessage.objects.create(thread=self.friend_thread, user=self.thread.user, text=message)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    def chat_message(self, event):
        message = event['message']
        username = event['username']

        self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))





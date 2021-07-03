from chatter.models import ChatData
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import random

#LOADING FILE
f = open('data.json',)
data = json.load(f)
count = 10

class ChatConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def store_user(self,user):
        chat_data,_ = ChatData.objects.get_or_create(user = user)
        chat_data.room_name = self.room_name
        chat_data.save()

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        user = self.scope['user']
        await self.store_user(user)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    @database_sync_to_async
    def store_chunk(self,user,count):
        chat_data = ChatData.objects.get(user = user)
        chat_data.chunk_number = count
        chat_data.save()
        print(chat_data.chunk_number)


    async def chat_message(self, event):
        global count
        message = event['message']
        if message == 'START':
            await self.send(text_data=json.dumps({
            'message': data[:10]
        })) 
            print(data[:10])   
        elif message=='NEXT':
            await self.send(text_data=json.dumps({
                'message': data[count:count+10]
            }))
            print(data[count:count+10])
            count +=10
            user = self.scope['user']
            await self.store_chunk(user,count)
        else:
            await self.send(text_data=json.dumps({
                'message': 'enter a valid command'
            }))



f.close()
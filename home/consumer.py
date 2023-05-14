from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from .models import Order, Pizza
from django.contrib.auth import get_user_model

User = get_user_model()


class OrderConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = 'order_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

        order = Order.give_order_details(self.room_name)
        self.send(json.dumps(order))

    def disconnect(self, code):
        print(code)
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        super().disconnect(code)

    def order_status(self, event):
        data = json.loads(event['value'])
        self.send(json.dumps(data))


class PizzaConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'pizza'
        self.room_group_name = 'order_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

        order = Pizza.getAllPizzas()
        self.send(json.dumps(order))

    def receive(self, text_data):
        data = json.loads(text_data)
        if data['action'] == 'order':
            self.pizza_order(data['pizza'], data['user'], data['amount'])

    def pizza_order(self, pizza_name, user_name, amount):
        user = User.objects.get(username=user_name)
        pizza = Pizza.objects.get(name=pizza_name)

        order = Order(pizza=pizza, user=user, amount=amount)
        order.save()

    def order_status(self, event):
        data = json.loads(event['value'])
        self.send(json.dumps(data))

    def disconnect(self, code):
        return super().disconnect(code)


class OrderUserConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['user_name']
        self.room_group_name = 'order_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

        order = Order.give_user_details(self.room_name)
        self.send(json.dumps(order))

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        super().disconnect(code)

    def receive(self, text_data):
        data = json.loads(text_data)
        if data['action'] == 'delete':            
            self.delete_order(data['order_id'])

    def delete_order(self, order_id):
        order = Order.objects.get(order_id=order_id)
        order.delete()

    def order_status(self, event):
        data = json.loads(event['value'])
        self.send(json.dumps(data))

from django.db import models
import string
import random
import json
from django.contrib.auth.models import User
from django.dispatch import receiver

from asgiref.sync import async_to_sync

from django.db.models.signals import post_save, post_delete
from channels.layers import get_channel_layer


# Create your models here.
class Pizza(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=100)
    image = models.CharField(max_length=1024)

    def __str__(self):
        return self.name

    @staticmethod
    def getAllPizzas():
        pizzas = Pizza.objects.all()
        data = []
        for pizza in pizzas:
            temp = {}
            temp['name'] = pizza.name
            temp['price'] = pizza.price
            temp['image'] = pizza.image
            data.append(temp)

        return data


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


CHOICES = (
    ("Order Recieved", "Order Recieved"),
    ("Order Baking", "Order Baking"),
    ("Order Baked", "Order Baked"),
    ("Order Out for Delivery", "Order Out for Delivery"),
    ("Order Delivered", "Order Delivered"),
)


class Order(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100, blank=True)
    amount = models.IntegerField(default=100)
    status = models.CharField(
        max_length=100, choices=CHOICES, default='Order Recieved')
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not len(self.order_id):
            self.order_id = random_string_generator()

        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return self.order_id

    @staticmethod
    def give_user_details(username):
        user = User.objects.get(username=username)
        orders = Order.objects.filter(user=user)

        data = []

        for order in orders:
            temp = {}
            temp['order_id'] = order.order_id
            temp['pizza'] = order.pizza.name
            temp['amount'] = order.amount
            temp['status'] = order.status
            progress = 0
            if order.status == 'Order Recieved':
                progress = 20
            elif order.status == 'Order Baking':
                progress = 40
            elif order.status == 'Order Baked':
                progress = 60
            elif order.status == 'Order Out for Delivery':
                progress = 80
            elif order.status == 'Order Delivered':
                progress = 100

            temp['progress'] = progress

            data.append(temp)

        return data

    @staticmethod
    def give_order_details(order_id):
        instance = Order.objects.get(order_id=order_id)

        data = {}
        data['order_id'] = instance.order_id
        data['amount'] = instance.amount
        data['status'] = instance.status

        progress = 0
        if instance.status == 'Order Recieved':
            progress = 20
        elif instance.status == 'Order Baking':
            progress = 40
        elif instance.status == 'Order Baked':
            progress = 60
        elif instance.status == 'Order Out for Delivery':
            progress = 80
        elif instance.status == 'Order Delivered':
            progress = 100

        data['progress'] = progress

        return data


@receiver(post_save, sender=Pizza)
def pizza_data_handler(sender, instance, created, **kwargs):
    # if not created:
    channel_layer = get_channel_layer()

    pizzas = Pizza.objects.all()
    data = []
    for pizza in pizzas:
        temp = {}
        temp['name'] = pizza.name
        temp['price'] = pizza.price
        temp['image'] = pizza.image
        data.append(temp)

    async_to_sync(channel_layer.group_send)(
        'order_pizza', {
            'type': 'order_status',
            'value': json.dumps(data)
        }
    )


@receiver(post_save, sender=Order)
def order_status_handler(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    if not created:
        ################### sending to that specific order######################

        data = {}
        data['order_id'] = instance.order_id
        data['amount'] = instance.amount
        data['status'] = instance.status

        progress = 0
        if instance.status == 'Order Recieved':
            progress = 20
        elif instance.status == 'Order Baking':
            progress = 40
        elif instance.status == 'Order Baked':
            progress = 60
        elif instance.status == 'Order Out for Delivery':
            progress = 80
        elif instance.status == 'Order Delivered':
            progress = 100

        data['progress'] = progress

        async_to_sync(channel_layer.group_send)(
            'order_%s' % instance.order_id, {
                'type': 'order_status',
                'value': json.dumps(data)
            }
        )

        ############## here I am sending to that specific user#################

        user = instance.user
        orders = Order.objects.filter(user=user)

        data = []

        for order in orders:
            temp = {}
            temp['order_id'] = order.order_id
            temp['pizza'] = order.pizza.name
            temp['amount'] = order.amount
            temp['status'] = order.status
            progress = 0
            if order.status == 'Order Recieved':
                progress = 20
            elif order.status == 'Order Baking':
                progress = 40
            elif order.status == 'Order Baked':
                progress = 60
            elif order.status == 'Order Out for Delivery':
                progress = 80
            elif order.status == 'Order Delivered':
                progress = 100

            temp['progress'] = progress

            data.append(temp)

        async_to_sync(channel_layer.group_send)(
            'order_%s' % user.username, {
                'type': 'order_status',
                'value': json.dumps(data)
            }
        )

    else:
        user = instance.user
        orders = Order.objects.filter(user=user)

        data = []

        for order in orders:
            temp = {}
            temp['order_id'] = order.order_id
            temp['pizza'] = order.pizza.name
            temp['amount'] = order.amount
            temp['status'] = order.status
            progress = 0
            if order.status == 'Order Recieved':
                progress = 20
            elif order.status == 'Order Baking':
                progress = 40
            elif order.status == 'Order Baked':
                progress = 60
            elif order.status == 'Order Out for Delivery':
                progress = 80
            elif order.status == 'Order Delivered':
                progress = 100

            temp['progress'] = progress

            data.append(temp)

        async_to_sync(channel_layer.group_send)(
            'order_%s' % user.username, {
                'type': 'order_status',
                'value': json.dumps(data)
            }
        )


@receiver(post_delete, sender=Order)
def order_delete_handler(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    user = instance.user
    orders = Order.objects.filter(user=user)

    data = []

    for order in orders:
        temp = {}
        temp['order_id'] = order.order_id
        temp['pizza'] = order.pizza.name
        temp['amount'] = order.amount
        temp['status'] = order.status

        data.append(temp)

    async_to_sync(channel_layer.group_send)(
        'order_%s' % user.username, {
            'type': 'order_status',
            'value': json.dumps(data)
        }
    )

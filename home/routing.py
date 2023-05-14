from channels.routing import URLRouter
from django.urls import path
from .consumer import *

ws_patterns = URLRouter([
    path('order/id/<order_id>', OrderConsumer.as_asgi()),
    path('order/user/<user_name>', OrderUserConsumer.as_asgi()),
    path('pizza', PizzaConsumer.as_asgi()),
])
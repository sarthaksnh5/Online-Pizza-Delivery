from channels.routing import URLRouter
from django.urls import path
from home import routing as homeRouting

ws_patterns = URLRouter([
    path('ws/home/', homeRouting.ws_patterns)
])
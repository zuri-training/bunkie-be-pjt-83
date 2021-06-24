from django.urls import path
from .views import *

urlpatterns = [
    path('filter/', room_filter, name='filter')
]
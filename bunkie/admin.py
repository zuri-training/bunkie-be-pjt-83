from django.contrib import admin
from .models import User, Room

# Register your models here.
admin.site.register(User, Room)
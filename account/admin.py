from django.contrib import admin
from .models import User, LandLord, Student

# Register your models here.
admin.site.register(User)
admin.site.register(LandLord)
admin.site.register(Student)

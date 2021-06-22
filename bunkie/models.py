from django.db import models

ROOM_CHOICES = (
    ("Double Double", "Double Double"),
    ("Quad", "Quad"),
    ("4 Person", "4 Person"),
    ("Double", "Double"),
    ("Twin", "Twin"),
    ("Dorm", "Dorm")
)

ROOMMATES_CHOICES = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8")
)

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length = 25)
    last_name = models.CharField(max_length = 25)
    email = models.EmailField()

class Room(models.Model):
    room_type = models.CharField(
        max_length = 20,
        choices = ROOM_CHOICES,
        default = 'Double'
    )
    description = models.TextField()
    location = models.CharField(max_length = 400)
    no_of_roommates = models.CharField(
        max_length = 20,
        choices = ROOMMATES_CHOICES,
        default = '1'
    )
    price = models.SmallIntegerField()
    rental_period = models.DurationField()
    photo = models.ImageField(upload_to = 'uploads/', height_field = 100, width_field = 100)
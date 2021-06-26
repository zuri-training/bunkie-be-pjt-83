from account.models import User
from django.db import models
from account.models import  LandLord, User


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


############### Room model #########################################
############### Created by Baiye Moyosore #################

class Room(models.Model):
    landlord = models.ForeignKey(LandLord, related_name='landlords', on_delete=models.CASCADE)
    room_type = models.CharField(max_length = 20,choices = ROOM_CHOICES,default = 'Double')
    description = models.TextField()
    state = models.CharField(max_length = 400,blank=True)
    university = models.CharField(max_length=500,blank=True)
    no_of_roommates = models.CharField(max_length = 20,choices = ROOMMATES_CHOICES,default = '1')
    type_of_apartment = models.CharField(max_length=400, blank=True)
    price = models.SmallIntegerField()
    rental_period = models.DurationField()
    photo = models.ImageField(upload_to = 'uploads/', height_field = 100, width_field = 100, blank=True)


    def __str__(self):
        return str(self.room_type)




############################ Comments #################################
class Comment(models.Model): 
    post = models.ForeignKey(Room,
                             on_delete=models.CASCADE,
                             related_name='rooms')
    name = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE) 
    body = models.TextField() 
    created = models.DateTimeField(auto_now_add=True) 

    class Meta: 
        ordering = ('created',) 

    def __str__(self): 
        return 'Comment by {} on {}'.format(self.name, self.post) 
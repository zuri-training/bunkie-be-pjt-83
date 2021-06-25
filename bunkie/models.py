from django.db import models

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

# from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.conf import settings
from django.db.models.base import Model



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


########################## Generating Token for every User #################################################
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



##################################### Base User manager #########################################################
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, is_staff=False, is_active=True, is_admin=False, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        if not password:
            raise ValueError('user must have a password')

        user_obj = self.model(
            email=email,
            **extra_fields
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True,


        )
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
            is_admin=True,


        )
        return user


############################# account section ############################
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField( default=True)
    staff       = models.BooleanField(default=False)
    admin       = models.BooleanField(default=False)
    phone = models.CharField(max_length=300, blank=True)
    address = models.CharField(max_length=300, blank=True)
    student_status = models.BooleanField(default=False)
    landlord_status = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):

        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active





############################ Student Account ########################
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    avatar = models.ImageField(upload_to='students/avatar/', null=True, blank=True)
    full_name = models.CharField( max_length=30, blank=True)
    gender = models.CharField(max_length=100,blank=True)
    state_of_origin = models.CharField(max_length=400,blank=True)
    university = models.CharField(max_length=500,blank=True)
    department = models.CharField(max_length=500,blank=True)
    facebook_handle = models.CharField(max_length=700,blank=True)
    twitter_handle = models.CharField(max_length=700,blank=True)
    instagram_handle = models.CharField(max_length=700,blank=True)
    personal_interest = models.TextField()
    student_id = models.ImageField(upload_to='students/id/', null=True, blank=True)


 ########################3 Landlord account ###############################
class LandLord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=300)
    lastname_name = models.CharField(max_length=300)
    address = models.TextField()
    avatar = models.ImageField(upload_to='landlords/avatar/', null=True, blank=True)
    gender = models.CharField(max_length=100)



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
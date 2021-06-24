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



##################################### Base User manager #########################################################
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


############################# account section ############################
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField( default=True)
    phone = models.CharField(max_length=300, blank=True)
    address = models.CharField(max_length=300, blank=True)
    student_status = models.BooleanField(default=False)
    landlord_status = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email





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



############### Room model #########################################33

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
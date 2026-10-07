from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager

class User(AbstractUser):
    """Custom user model to extend the default user model"""
    email = models.EmailField(unique=True,db_index=True)

    objects = CustomUserManager()
    
    def __str__(self):
        return self.email


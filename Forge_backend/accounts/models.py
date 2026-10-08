from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager

class User(AbstractUser):
    """Custom user model to extend the default user model
    using email as the unique identifier instead of username.
    """
    username = None
    email = models.EmailField(unique=True,db_index=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    
    def __str__(self):
        return self.email


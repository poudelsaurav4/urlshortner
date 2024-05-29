from django.db import models
import random
import string
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.utils import timezone
from .manager import CustomUserManager

# Create your models here.

# class RegisterUser(models.Model):
#     email = models.EmailField(unique=True)
#     username = models.CharField(max_length=255, unique=True)
#     password = models.CharField(max_length=255)

#     def __str__(self):
#         return self.username
    
    # gender_choices = (
    #     ('M', "male"),
    #     ("F", "Female"),
    #     ("o","others")   
    # )
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateField(default= timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def __str__(self) -> str:
        return self.username

class UrlData(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name = 'user')
    url = models.CharField(max_length=255)
    short_url = models.CharField(max_length=20)
    
    def __str__(self) -> str:
        # return f"your url was: {self.url}, shortened is: {self.short_url}"
        return self.url

    def save(self, *args, **kwargs):
        if not self.pk:
            self.short_url = self.gen_short_url()
        return super().save(*args, **kwargs)
        
    def gen_short_url(self):
        chars = string.ascii_letters
        short_url = ' '.join(random.choice(chars)for _ in range(6))

        return short_url
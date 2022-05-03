from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile/")



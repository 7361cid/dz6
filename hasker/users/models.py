from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_avatar = models.ImageField(null=True, blank=True, upload_to="images/profile/",
                                       default='images/deafult-profile-image.png')

    @staticmethod
    def get_avatar(pk):
        try:
            return CustomUser.objects.get(pk=pk).profile_avatar
        except CustomUser.DoesNotExist:
            return 'images/deafult-profile-image.png'


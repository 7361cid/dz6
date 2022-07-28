from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_avatar = models.ImageField(null=True, blank=True, upload_to="images/profile/",
                                       default='images/deafult-profile-image.png')

    def get_avatar(self):
        if self.profile_avatar:
            return self.profile_avatar
        else:
            return 'images/deafult-profile-image.png'


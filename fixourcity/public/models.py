from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_admin = models.BooleanField('Is admin', default=False)
    is_contractor = models.BooleanField('Is contractor', default=False)
    is_authority = models.BooleanField('Is authority', default=False)
    is_users = models.BooleanField('Is regular user', default=False)

    def __str__(self):
        return self.username

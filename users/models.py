from django.contrib.auth.models import AbstractUser
from django.db import models

from blog.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=254, unique=True, verbose_name='e-mail')
    phone = models.CharField(max_length=35, verbose_name='телефон')
    country = models.CharField(max_length=100, verbose_name='страна')
    profile_img = models.ImageField(upload_to='users/profile_imgs/', verbose_name='аватар', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

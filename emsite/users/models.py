from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    second_name = models.CharField('Отчество', max_length=100,blank=True)


    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'
        verbose_name = 'Имя пользователя'
        verbose_name_plural = 'Мои пользователи'

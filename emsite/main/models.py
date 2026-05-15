from datetime import time

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# Create your models here.

class Office(models.Model):
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=100)
    time_work_from = models.TimeField(default=time(10, 0))
    time_work_to = models.TimeField(default=time(18, 0))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Офисы'
        verbose_name_plural = 'Офисы'


class Staff(models.Model):
    offices = models.ManyToManyField(Office, default=None, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} {self.offices}'


class Day(models.Model):
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    date = models.DateField()
    from_time = models.TimeField(blank=True, null=True)
    to_time = models.TimeField(blank=True, null=True)

    def save(self, *args, **kwargs):

        if not self.from_time:
            self.from_time = self.office.time_work_from

        if not self.to_time:
            self.to_time = self.office.time_work_to

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.date}: {self.from_time}-{self.to_time}'


class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    from_time = models.TimeField()
    to_time = models.TimeField()

    def __str__(self):
        return f'{self.day.date}: {self.from_time}-{self.to_time}'

    class Meta:
        db_table = 'schedules'
        verbose_name = 'Записи'
        verbose_name_plural = 'Записи'


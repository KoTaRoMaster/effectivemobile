import calendar
from datetime import time, date, timedelta

from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Staff, Day, Schedule, Office

User = get_user_model()


@receiver(pre_save, sender=User)
def track_staff_status_change(sender, instance, **kwargs):
    if instance.pk:
        old_instance = User.objects.get(pk=instance.pk)
        instance._old_is_staff = old_instance.is_staff
        instance._old_is_superuser = old_instance.is_superuser
    else:
        instance._old_is_staff = False


@receiver(post_save, sender=User)
def handle_staff_status_change(sender, instance, created, **kwargs):
    # Для новых пользователей=
    if created:
        if instance.is_staff or instance.is_superuser:
            Staff.objects.create(user=instance)
    else:
        # Для существующих - проверяем изменилось ли поле
        old_is_staff = getattr(instance, '_old_is_staff', False)

        if (instance.is_staff and not old_is_staff) or (instance.is_superuser and not old_is_staff):
            # Стал сотрудником
            Staff.objects.create(user=instance)
        elif (not instance.is_staff and old_is_staff) and (not instance.is_superuser and old_is_staff):
            # Перестал быть сотрудником
            Staff.objects.filter(user=instance).delete()


@receiver(post_save, sender=Office)
def create_days(sender, instance, created, **kwargs):
    if created:

        today = date.today()

        first_day = date(today.year, today.month, 1)

        days_in_month = calendar.monthrange(
            today.year,
            today.month
        )[1]

        days = []

        for i in range(days_in_month):
            days.append(
                Day(
                    office=instance,
                    date=first_day + timedelta(days=i),
                    from_time=instance.time_work_from,
                    to_time=instance.time_work_to
                )
            )

        created_days = Day.objects.bulk_create(days)

        schedules = []

        for day in created_days:
            from_h, from_m = [int(time_) for time_ in day.from_time.strftime("%H:%M").split(":")]
            to_h, to_m = [int(time_) for time_ in day.to_time.strftime("%H:%M").split(":")]
            h, m = to_h - from_h, to_m - from_m
            quantity_intervals = h * 2 + (m // 30)
            dh, dm = 0, 0,
            for i in range(quantity_intervals):
                dmh = dm + 30
                schedule = Schedule(
                    day=day,
                    from_time=time(from_h + dh, from_m + dm),
                    to_time=time(from_h + dh + dmh // 60, from_m + dmh % 60)
                )
                dm += 30
                if dm > 30:
                    dm = 0
                    dh += 1
                schedules.append(schedule)
        Schedule.objects.bulk_create(schedules)

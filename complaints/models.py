from django.contrib.auth.models import User
from django.db import models

from machines.models import Machine


class FailureNode(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название',
    )
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Узел отказа'
        verbose_name_plural = 'Узлы отказа'

    def __str__(self):
        return self.name


class RecoveryMethod(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название',
    )
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Способ восстановления'
        verbose_name_plural = 'Способы восстановления'

    def __str__(self):
        return self.name


class Complaint(models.Model):
    failure_date = models.DateField(verbose_name='Дата отказа')
    operating_time = models.IntegerField(verbose_name='Наработка, м/час')
    failure_node = models.ForeignKey(
        FailureNode,
        on_delete=models.CASCADE,
        verbose_name='Узел отказа',
    )
    failure_description = models.TextField(verbose_name='Описание отказа')
    recovery_method = models.ForeignKey(
        RecoveryMethod,
        on_delete=models.CASCADE,
        verbose_name='Способ восстановления',
    )
    spare_parts = models.TextField(
        blank=True,
        verbose_name='Используемые запасные части',
    )
    recovery_date = models.DateField(verbose_name='Дата восстановления')
    downtime = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Время простоя техники',
    )
    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE,
        verbose_name='Машина',
    )
    service_company = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Сервисная компания',
    )

    class Meta:
        verbose_name = 'Рекламация'
        verbose_name_plural = 'Рекламации'

    def save(self, *args, **kwargs):
        # Downtime is calculated from the failure and recovery dates.
        self.downtime = (self.recovery_date - self.failure_date).days
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.machine} - {self.failure_date}'

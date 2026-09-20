from django.contrib.auth.models import User
from django.db import models

from machines.models import Machine


class MaintenanceType(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название',
    )
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Вид ТО'
        verbose_name_plural = 'Виды ТО'

    def __str__(self):
        return self.name


class MaintenanceOrganization(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название',
    )
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Организация, проводившая ТО'
        verbose_name_plural = 'Организации, проводившие ТО'

    def __str__(self):
        return self.name


class Maintenance(models.Model):
    maintenance_type = models.ForeignKey(
        MaintenanceType,
        on_delete=models.CASCADE,
        verbose_name='Вид ТО',
    )
    maintenance_date = models.DateField(verbose_name='Дата проведения ТО')
    operating_time = models.IntegerField(verbose_name='Наработка, м/час')
    work_order_number = models.CharField(
        max_length=255,
        verbose_name='№ заказ-наряда',
    )
    work_order_date = models.DateField(verbose_name='Дата заказ-наряда')
    organization = models.ForeignKey(
        MaintenanceOrganization,
        on_delete=models.CASCADE,
        verbose_name='Организация, проводившая ТО',
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
        verbose_name = 'ТО'
        verbose_name_plural = 'ТО'

    def __str__(self):
        return f'{self.machine} - {self.maintenance_type}'

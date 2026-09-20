from django.contrib.auth.models import User
from django.db import models


class TechniqueModel(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Модель техники'
        verbose_name_plural = 'Модели техники'

    def __str__(self):
        return self.name


class EngineModel(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Модель двигателя'
        verbose_name_plural = 'Модели двигателя'

    def __str__(self):
        return self.name


class TransmissionModel(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Модель трансмиссии'
        verbose_name_plural = 'Модели трансмиссии'

    def __str__(self):
        return self.name


class DriveAxleModel(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Модель ведущего моста'
        verbose_name_plural = 'Модели ведущего моста'

    def __str__(self):
        return self.name


class SteeringAxleModel(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Модель управляемого моста'
        verbose_name_plural = 'Модели управляемого моста'

    def __str__(self):
        return self.name


class Machine(models.Model):
    factory_number = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Зав. № машины',
    )
    technique_model = models.ForeignKey(
        TechniqueModel,
        on_delete=models.CASCADE,
        verbose_name='Модель техники',
    )
    engine_model = models.ForeignKey(
        EngineModel,
        on_delete=models.CASCADE,
        verbose_name='Модель двигателя',
    )
    engine_factory_number = models.CharField(
        max_length=255,
        verbose_name='Зав. № двигателя',
    )
    transmission_model = models.ForeignKey(
        TransmissionModel,
        on_delete=models.CASCADE,
        verbose_name='Модель трансмиссии',
    )
    transmission_factory_number = models.CharField(
        max_length=255,
        verbose_name='Зав. № трансмиссии',
    )
    drive_axle_model = models.ForeignKey(
        DriveAxleModel,
        on_delete=models.CASCADE,
        verbose_name='Модель ведущего моста',
    )
    drive_axle_factory_number = models.CharField(
        max_length=255,
        verbose_name='Зав. № ведущего моста',
    )
    steering_axle_model = models.ForeignKey(
        SteeringAxleModel,
        on_delete=models.CASCADE,
        verbose_name='Модель управляемого моста',
    )
    steering_axle_factory_number = models.CharField(
        max_length=255,
        verbose_name='Зав. № управляемого моста',
    )
    supply_contract = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Договор поставки №, дата',
    )
    shipment_date = models.DateField(verbose_name='Дата отгрузки с завода')
    consignee = models.CharField(
        max_length=255,
        verbose_name='Грузополучатель (конечный потребитель)',
    )
    delivery_address = models.CharField(
        max_length=255,
        verbose_name='Адрес поставки (эксплуатации)',
    )
    equipment = models.TextField(
        blank=True,
        verbose_name='Комплектация (доп. опции)',
    )

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='client_machines',
        verbose_name='Клиент',
    )
    service_company = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='service_company_machines',
        verbose_name='Сервисная компания',
    )

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'

    def __str__(self):
        return self.factory_number

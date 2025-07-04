from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError


class DistributionNetwork(models.Model):
    """
    Сеть дистрибуции
    """

    factory = models.ForeignKey(
        "NetworkParticipant",
        on_delete=models.SET_NULL,
        limit_choices_to={"type": "factory"},
        null=True,
        related_name="factories",
    )  # Завод
    retail_network = models.ForeignKey(
        "NetworkParticipant",
        on_delete=models.SET_NULL,
        limit_choices_to={"type": "retail_network"},
        null=True,
        blank=True,
        related_name="retail_networks",
    )  # Розничная сеть
    individual_entrepreneur = models.ForeignKey(
        "NetworkParticipant",
        on_delete=models.SET_NULL,
        limit_choices_to={"type": "individual_entrepreneur"},
        null=True,
        blank=True,
        related_name="individual_entrepreneurs",
    )  # Индивидуальный предприниматель

    class Meta:
        verbose_name = "Сеть дистрибуции"
        verbose_name_plural = "Сети дистрибуции"


class NetworkParticipant(models.Model):
    """
    Участник сети дистрибуции
    """

    class Types(models.TextChoices):
        FACTORY = "factory", "Завод"
        RETAIL_NETWORK = "retail_network", "Розничная сеть"
        INDIVIDUAL_ENTREPRENEUR = "individual_entrepreneur", "ИП"

    type = models.CharField(max_length=25, choices=Types.choices)
    name = models.CharField(max_length=255, verbose_name="Название")

    # Контакты
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    country = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Страна"
    )
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Город")
    street = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Улица"
    )
    house_number = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Номер дома"
    )

    products = models.ManyToManyField(
        "Product",
        blank=True,
        verbose_name="Продукты",
        related_name="network_participant",
    )

    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Поставщик",
        related_name="clients",
    )
    debt_to_supplier = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        default=Decimal("0.00"),
        verbose_name="Задолженность перед поставщиком",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    class Meta:
        verbose_name = "Участник сети"
        verbose_name_plural = "Участники сети"

    def __str__(self):
        return f"{self.get_type_display()}: {self.name}"

    def clean(self):
        """
        Проверка, что завод не может иметь поставщика
        """
        if self.type == self.Types.FACTORY and self.supplier:
            raise ValidationError("Завод не может иметь поставщика")


class Product(models.Model):
    """
    Продукт
    """

    name = models.CharField(max_length=255, verbose_name="Название")
    model = models.CharField(max_length=255, verbose_name="Модель")
    realese_date = models.DateField(verbose_name="Дата выхода продукта на рынок")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name

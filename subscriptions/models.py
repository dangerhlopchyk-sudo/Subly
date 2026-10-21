import calendar
import datetime
from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models
from django.urls import reverse

from .validators import validate_icon, validate_not_blank, validate_reasonable_date


def add_months(date, months):
    month_index = date.month - 1 + months
    year = date.year + month_index // 12
    month = month_index % 12 + 1
    day = min(date.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


class Category(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(
        "Назва",
        max_length=40,
        validators=[MinLengthValidator(2), validate_not_blank],
    )
    color = models.CharField(
        "Колір",
        max_length=7,
        default="#3fb8f6",
        validators=[RegexValidator(r"^#[0-9a-fA-F]{6}$", "Колір у форматі #rrggbb")],
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "категорія"
        verbose_name_plural = "категорії"
        constraints = [
            models.UniqueConstraint(fields=["user", "name"], name="unique_category_per_user"),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("subscriptions:category_detail", args=[self.pk])


class Tag(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Власник", on_delete=models.CASCADE)
    name = models.CharField(
        "Назва",
        max_length=30,
        validators=[MinLengthValidator(2), validate_not_blank],
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "тег"
        verbose_name_plural = "теги"
        constraints = [
            models.UniqueConstraint(fields=["user", "name"], name="unique_tag_per_user"),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("subscriptions:tag_detail", args=[self.pk])


class Subscription(models.Model):
    class Cycle(models.TextChoices):
        MONTH = "month", "Щомісяця"
        YEAR = "year", "Щороку"

    class Status(models.TextChoices):
        ACTIVE = "active", "Активна"
        PAUSED = "paused", "На паузі"
        CANCELLED = "cancelled", "Скасована"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(
        "Назва",
        max_length=100,
        validators=[MinLengthValidator(2), validate_not_blank],
    )
    service = models.CharField("Сервіс з каталогу", max_length=40, blank=True, default="")
    icon = models.FileField(
        "Своє зображення", upload_to="sub_icons/", blank=True, validators=[validate_icon]
    )
    category = models.ForeignKey(
        Category, verbose_name="Категорія", on_delete=models.SET_NULL, null=True, blank=True
    )
    price = models.DecimalField(
        "Вартість, ₴",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01")), MaxValueValidator(Decimal("1000000"))],
    )
    billing_cycle = models.CharField(
        "Періодичність", max_length=5, choices=Cycle.choices, default=Cycle.MONTH
    )
    next_payment_date = models.DateField("Наступний платіж", validators=[validate_reasonable_date])
    last_paid_date = models.DateField("Остання оплата", null=True, blank=True)
    status = models.CharField(
        "Статус", max_length=10, choices=Status.choices, default=Status.ACTIVE
    )
    auto_renew = models.BooleanField("Автопродовження", default=True)
    tags = models.ManyToManyField(Tag, verbose_name="Теги", related_name="subscriptions", blank=True)
    notes = models.TextField("Нотатки", blank=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["next_payment_date", "name"]
        verbose_name = "підписка"
        verbose_name_plural = "підписки"
        permissions = [("view_all_stats", "Може переглядати статистику всіх користувачів")]
        constraints = [
            models.CheckConstraint(condition=models.Q(price__gt=0), name="price_positive"),
            models.UniqueConstraint(fields=["user", "name"], name="unique_subscription_per_user"),
        ]

    def __str__(self):
        return f"{self.name} ({self.price} ₴)"

    def get_absolute_url(self):
        return reverse("subscriptions:detail", args=[self.pk])

    def clean(self):
        if self.price is not None and self.price <= 0:
            raise ValidationError({"price": "Вартість мусить бути більшою за 0"})

    @property
    def is_active(self):
        return self.status == self.Status.ACTIVE

    @property
    def monthly_cost(self):
        if self.billing_cycle == self.Cycle.YEAR:
            return (self.price / 12).quantize(Decimal("0.01"))
        return self.price

    @property
    def yearly_cost(self):
        if self.billing_cycle == self.Cycle.YEAR:
            return self.price
        return self.price * 12

    @property
    def days_left(self):
        return (self.next_payment_date - datetime.date.today()).days

    @property
    def payment_state(self):
        if not self.is_active:
            return "inactive"
        if self.days_left < 0:
            return "overdue"
        if self.days_left <= 7:
            return "soon"
        return "scheduled"

    @property
    def state_label(self):
        if not self.is_active:
            return self.get_status_display()
        return {
            "overdue": "Прострочено",
            "soon": "Скоро",
            "scheduled": "Заплановано",
        }[self.payment_state]

    @property
    def when_label(self):
        d = self.days_left
        if d == 0:
            return "сьогодні"
        if d == 1:
            return "завтра"
        if d < 0:
            return f"{-d} дн. тому"
        return f"через {d} дн."

    def mark_paid(self):
        step = 12 if self.billing_cycle == self.Cycle.YEAR else 1
        today = datetime.date.today()
        Payment.objects.create(subscription=self, amount=self.price, paid_date=today)
        self.last_paid_date = today
        self.next_payment_date = add_months(self.next_payment_date, step)
        while self.next_payment_date <= today:
            self.next_payment_date = add_months(self.next_payment_date, step)
        self.save()


class Payment(models.Model):
    subscription = models.ForeignKey(
        Subscription, verbose_name="Підписка", related_name="payments", on_delete=models.CASCADE
    )
    amount = models.DecimalField(
        "Сума, ₴",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    paid_date = models.DateField("Дата оплати")
    note = models.CharField("Примітка", max_length=200, blank=True)

    class Meta:
        ordering = ["-paid_date", "-id"]
        verbose_name = "платіж"
        verbose_name_plural = "платежі"

    def __str__(self):
        return f"{self.subscription.name}: {self.amount} ₴ ({self.paid_date:%d.%m.%Y})"

    def get_absolute_url(self):
        return reverse("subscriptions:payment_detail", args=[self.pk])

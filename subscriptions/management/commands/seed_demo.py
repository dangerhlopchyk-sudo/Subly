import datetime
from decimal import Decimal

from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

from subscriptions.catalog import find_by_name
from subscriptions.apps import MANAGER_GROUP
from subscriptions.models import Category, Payment, Subscription, Tag

DEMO = [
    ("Spotify", "Музика", "99", "month", 20, 10),
    ("Netflix", "Стрімінг", "299", "month", 22, 8),
    ("YouTube Premium", "Стрімінг", "159", "month", 1, None),
    ("Microsoft OneDrive", "Хмара", "1990", "year", 40, None),
    ("ChatGPT", "ШІ", "840", "month", 12, None),
    ("Duolingo", "Навчання", "2300", "year", 90, None),
    ("Xbox Game Pass", "Ігри", "349", "month", 9, None),
    ("iCloud", "Хмара", "49", "month", -2, None),
    ("Notion", "Софт", "420", "month", 5, None),
    ("Claude", "ШІ", "830", "month", 3, None),
    ("Київстар", "Зв'язок", "250", "month", 6, 25),
    ("Невідомий сервіс", "Інше", "75", "month", 15, None),
]


class Command(BaseCommand):
    help = "Створює demo / demo12345, менеджера manager / manager12345, підписки, теги й платежі"

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(username="demo", defaults={"email": "demo@example.com"})
        if created:
            user.set_password("demo12345")
            user.save()
        today = datetime.date.today()
        for name, cat, price, cycle, days, paid_ago in DEMO:
            Subscription.objects.get_or_create(
                user=user,
                name=name,
                defaults={
                    "service": (find_by_name(name) or {}).get("slug", ""),
                    "category": Category.objects.filter(user=None, name=cat).first(),
                    "price": Decimal(price),
                    "billing_cycle": cycle,
                    "next_payment_date": today + datetime.timedelta(days=days),
                    "last_paid_date": today - datetime.timedelta(days=paid_ago) if paid_ago else None,
                },
            )
        work, _ = Tag.objects.get_or_create(user=user, name="Робота")
        family, _ = Tag.objects.get_or_create(user=user, name="Сімейне")
        for name, tag in (("ChatGPT", work), ("Notion", work), ("Netflix", family), ("Spotify", family)):
            sub = Subscription.objects.filter(user=user, name=name).first()
            if sub:
                sub.tags.add(tag)
                if not sub.payments.exists():
                    Payment.objects.create(subscription=sub, amount=sub.price, paid_date=today - datetime.timedelta(days=9))

        manager, created = User.objects.get_or_create(username="manager", defaults={"email": "manager@example.com"})
        if created:
            manager.set_password("manager12345")
            manager.save()
        group, _ = Group.objects.get_or_create(name=MANAGER_GROUP)
        manager.groups.add(group)
        self.stdout.write(self.style.SUCCESS("Готово. Вхід: demo / demo12345, менеджер: manager / manager12345"))

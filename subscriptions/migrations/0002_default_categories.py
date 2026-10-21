from django.db import migrations

DEFAULTS = [
    ("Стрімінг", "#ef4444"),
    ("Музика", "#22c55e"),
    ("Хмара", "#38bdf8"),
    ("Ігри", "#a855f7"),
    ("Навчання", "#f59e0b"),
    ("Софт", "#6366f1"),
    ("Інше", "#94a3b8"),
]


def create_defaults(apps, schema_editor):
    Category = apps.get_model("subscriptions", "Category")
    for name, color in DEFAULTS:
        Category.objects.get_or_create(user=None, name=name, defaults={"color": color})


def remove_defaults(apps, schema_editor):
    Category = apps.get_model("subscriptions", "Category")
    Category.objects.filter(user=None, name__in=[n for n, _ in DEFAULTS]).delete()


class Migration(migrations.Migration):
    dependencies = [("subscriptions", "0001_initial")]
    operations = [migrations.RunPython(create_defaults, remove_defaults)]

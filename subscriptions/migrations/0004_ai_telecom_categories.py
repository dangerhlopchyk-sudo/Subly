from django.db import migrations

NEW = [
    ("ШІ", "#14b8a6"),
    ("Зв'язок", "#f43f5e"),
    ("Інтернет", "#0ea5e9"),
]


def add_categories(apps, schema_editor):
    """Нові системні категорії для ШІ-сервісів, мобільного зв'язку та інтернет-провайдерів."""
    Category = apps.get_model("subscriptions", "Category")
    for name, color in NEW:
        Category.objects.get_or_create(user=None, name=name, defaults={"color": color})


def remove_categories(apps, schema_editor):
    Category = apps.get_model("subscriptions", "Category")
    Category.objects.filter(user=None, name__in=[n for n, _ in NEW]).delete()


class Migration(migrations.Migration):
    dependencies = [("subscriptions", "0003_subscription_service")]
    operations = [migrations.RunPython(add_categories, remove_categories)]

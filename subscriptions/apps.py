from django.apps import AppConfig
from django.db.models.signals import post_migrate

MANAGER_GROUP = "Менеджери"


def create_roles(sender, **kwargs):
    from django.contrib.auth.management import create_permissions
    from django.contrib.auth.models import Group, Permission

    create_permissions(sender, verbosity=0)
    group, _ = Group.objects.get_or_create(name=MANAGER_GROUP)
    permission = Permission.objects.filter(
        codename="view_all_stats", content_type__app_label="subscriptions"
    ).first()
    if permission:
        group.permissions.add(permission)


class SubscriptionsConfig(AppConfig):
    name = 'subscriptions'

    def ready(self):
        post_migrate.connect(create_roles, sender=self)

import django.core.validators
import django.db.models.deletion
import subscriptions.validators
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('subscriptions', '0005_subscription_icon'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscription',
            options={
                'ordering': ['next_payment_date', 'name'],
                'permissions': [('view_all_stats', 'Може переглядати статистику всіх користувачів')],
                'verbose_name': 'підписка',
                'verbose_name_plural': 'підписки',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(2), subscriptions.validators.validate_not_blank], verbose_name='Назва')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Власник')),
            ],
            options={
                'verbose_name': 'тег',
                'verbose_name_plural': 'теги',
                'ordering': ['name'],
            },
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='unique_tag_per_user'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='auto_renew',
            field=models.BooleanField(default=True, verbose_name='Автопродовження'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='subscriptions', to='subscriptions.tag', verbose_name='Теги'),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Сума, ₴')),
                ('paid_date', models.DateField(verbose_name='Дата оплати')),
                ('note', models.CharField(blank=True, max_length=200, verbose_name='Примітка')),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='subscriptions.subscription', verbose_name='Підписка')),
            ],
            options={
                'verbose_name': 'платіж',
                'verbose_name_plural': 'платежі',
                'ordering': ['-paid_date', '-id'],
            },
        ),
    ]

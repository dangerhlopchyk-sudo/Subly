# Generated
from django.db import migrations, models
import django.db.models.deletion
import django.core.validators
import subscriptions.validators
from decimal import Decimal
from django.conf import settings


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, validators=[django.core.validators.MinLengthValidator(2), subscriptions.validators.validate_not_blank], verbose_name='Назва')),
                ('color', models.CharField(default='#3fb8f6', max_length=7, validators=[django.core.validators.RegexValidator('^#[0-9a-fA-F]{6}$', 'Колір у форматі #rrggbb')], verbose_name='Колір')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'категорія',
                'verbose_name_plural': 'категорії',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(2), subscriptions.validators.validate_not_blank], verbose_name='Назва')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.01')), django.core.validators.MaxValueValidator(Decimal('1000000'))], verbose_name='Вартість, ₴')),
                ('billing_cycle', models.CharField(choices=[('month', 'Щомісяця'), ('year', 'Щороку')], default='month', max_length=5, verbose_name='Періодичність')),
                ('next_payment_date', models.DateField(validators=[subscriptions.validators.validate_reasonable_date], verbose_name='Наступний платіж')),
                ('last_paid_date', models.DateField(blank=True, null=True, verbose_name='Остання оплата')),
                ('status', models.CharField(choices=[('active', 'Активна'), ('paused', 'На паузі'), ('cancelled', 'Скасована')], default='active', max_length=10, verbose_name='Статус')),
                ('notes', models.TextField(blank=True, max_length=500, verbose_name='Нотатки')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='subscriptions.category', verbose_name='Категорія')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'підписка',
                'verbose_name_plural': 'підписки',
                'ordering': ['next_payment_date', 'name'],
            },
        ),
        migrations.AddConstraint(
            model_name='category',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='unique_category_per_user'),
        ),
        migrations.AddConstraint(
            model_name='subscription',
            constraint=models.CheckConstraint(condition=models.Q(('price__gt', 0)), name='price_positive'),
        ),
        migrations.AddConstraint(
            model_name='subscription',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='unique_subscription_per_user'),
        ),
    ]

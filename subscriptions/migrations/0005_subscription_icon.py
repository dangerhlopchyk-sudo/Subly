from django.db import migrations, models

import subscriptions.validators


class Migration(migrations.Migration):

    dependencies = [
        ("subscriptions", "0004_ai_telecom_categories"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscription",
            name="icon",
            field=models.FileField(
                blank=True,
                upload_to="sub_icons/",
                validators=[subscriptions.validators.validate_icon],
                verbose_name="Своє зображення",
            ),
        ),
    ]

# Generated by Django 5.1 on 2024-08-30 21:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("task_board", "0003_alter_task_options_alter_taskboard_options_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="dailytaskstats",
            name="user",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
            preserve_default=False,
        ),
    ]

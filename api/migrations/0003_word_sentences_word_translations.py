# Generated by Django 4.2.23 on 2025-06-20 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_language_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='sentences',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='word',
            name='translations',
            field=models.JSONField(blank=True, null=True),
        ),
    ]

# Generated by Django 4.0.6 on 2023-04-01 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0008_remove_timestamps_temp'),
    ]

    operations = [
        migrations.AddField(
            model_name='timestamps',
            name='temp',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 3.2.18 on 2023-07-11 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0002_processcontroller_total_acc'),
    ]

    operations = [
        migrations.AddField(
            model_name='processcontroller',
            name='list_data',
            field=models.JSONField(default=list),
        ),
    ]

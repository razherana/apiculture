# Generated by Django 5.2.3 on 2025-07-09 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projet', '0011_alter_intervention_localization_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='intervention',
            name='prix_service',
            field=models.FloatField(default=0),
        ),
    ]

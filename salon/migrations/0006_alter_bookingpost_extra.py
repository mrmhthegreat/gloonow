# Generated by Django 5.0.3 on 2024-03-13 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0005_services_bookingpost_delete_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingpost',
            name='extra',
            field=models.JSONField(null=True),
        ),
    ]

# Generated by Django 5.0.3 on 2024-03-14 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0006_alter_bookingpost_extra'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingpost',
            name='message',
            field=models.CharField(blank=True, default='', max_length=5000, null=True),
        ),
    ]

# Generated by Django 5.0.3 on 2024-05-30 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0026_remove_advancerequest_message_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advancerequest',
            name='user',
        ),
    ]

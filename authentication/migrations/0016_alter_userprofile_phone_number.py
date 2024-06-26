# Generated by Django 5.0.3 on 2024-04-28 10:30

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0015_alter_userprofile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='0064xxxxxxx format', max_length=128, region=None, unique=True),
        ),
    ]

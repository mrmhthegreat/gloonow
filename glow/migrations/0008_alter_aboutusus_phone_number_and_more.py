# Generated by Django 5.0.3 on 2024-04-28 11:02

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('glow', '0007_alter_aboutusus_text1_description2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutusus',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='0064xxxxxxx format', max_length=128, region='NZ', unique=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='0064xxxxxxx format', max_length=128, region='NZ', unique=True),
        ),
    ]

# Generated by Django 5.0.3 on 2024-04-28 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0016_alter_userprofile_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(default='', max_length=120),
        ),
    ]

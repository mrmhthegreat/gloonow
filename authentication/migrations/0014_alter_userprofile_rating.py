# Generated by Django 5.0.3 on 2024-03-17 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0013_alter_userprofile_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=1, default=0, max_digits=2, null=True),
        ),
    ]

# Generated by Django 5.0.3 on 2024-04-20 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('glow', '0003_aboutusus_logoimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aboutusus',
            old_name='comapnay',
            new_name='company',
        ),
    ]

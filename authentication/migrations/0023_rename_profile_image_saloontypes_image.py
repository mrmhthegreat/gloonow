# Generated by Django 4.2.7 on 2024-06-26 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0022_saloontypes_profile_image_userprofile_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='saloontypes',
            old_name='profile_image',
            new_name='image',
        ),
    ]
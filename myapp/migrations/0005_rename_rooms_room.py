# Generated by Django 4.0.4 on 2022-05-29 02:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_message_rooms'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Rooms',
            new_name='Room',
        ),
    ]
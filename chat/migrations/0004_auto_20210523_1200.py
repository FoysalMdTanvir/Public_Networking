# Generated by Django 3.0 on 2021-05-23 06:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_message_room'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.DeleteModel(
            name='Room',
        ),
    ]
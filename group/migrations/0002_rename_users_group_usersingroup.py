# Generated by Django 4.2 on 2024-03-02 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='users',
            new_name='usersInGroup',
        ),
    ]

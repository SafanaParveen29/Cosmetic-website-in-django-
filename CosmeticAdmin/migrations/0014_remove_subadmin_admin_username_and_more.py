# Generated by Django 4.2.7 on 2024-02-05 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CosmeticAdmin', '0013_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subadmin',
            name='admin_username',
        ),
        migrations.RemoveField(
            model_name='subadmin',
            name='password',
        ),
    ]

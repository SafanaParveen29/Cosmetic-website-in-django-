# Generated by Django 4.2.7 on 2024-02-05 05:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CosmeticAdmin', '0006_delete_subadmin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subadmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subadmin_username', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('subadmin_email', models.EmailField(max_length=254)),
                ('subadmin_Number', models.CharField(blank=True, max_length=10, null=True)),
                ('subadmin_password', models.CharField(max_length=255)),
                ('subadmin_password1', models.CharField(max_length=20)),
                ('admin_username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('Administator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CosmeticAdmin.administator')),
            ],
        ),
    ]

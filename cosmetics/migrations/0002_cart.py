# Generated by Django 4.2.7 on 2024-02-11 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CosmeticAdmin', '0016_alter_product_offerprice'),
        ('cosmetics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('cart_price', models.BigIntegerField(default=0)),
                ('status', models.CharField(max_length=50)),
                ('payment_status', models.CharField(max_length=50)),
                ('delivery_status', models.CharField(max_length=50)),
                ('Product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CosmeticAdmin.product')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cosmetics.customer')),
            ],
        ),
    ]

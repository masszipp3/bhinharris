# Generated by Django 4.2.1 on 2023-06-08 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_remove_product_stock_product_onstock'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='min_purchase',
            field=models.CharField(default='', max_length=10),
        ),
    ]

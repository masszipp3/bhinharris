# Generated by Django 4.2.1 on 2023-06-12 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0007_usercoupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='min_purchase',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]

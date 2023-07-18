# Generated by Django 4.2.1 on 2023-06-26 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0017_alter_product_final_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Price',
            field=models.DecimalField(decimal_places=1, max_digits=8),
        ),
        migrations.AlterField(
            model_name='product',
            name='final_total',
            field=models.DecimalField(decimal_places=1, max_digits=8),
        ),
    ]

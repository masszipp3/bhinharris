# Generated by Django 4.2.1 on 2023-06-26 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0020_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='final_total',
            field=models.IntegerField(),
        ),
    ]
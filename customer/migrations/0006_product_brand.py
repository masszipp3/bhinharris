# Generated by Django 4.2.1 on 2023-06-08 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_customer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(default='BHT', max_length=30),
        ),
    ]

# Generated by Django 4.2.1 on 2023-06-08 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsuser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_customer',
            field=models.BooleanField(default=False),
        ),
    ]
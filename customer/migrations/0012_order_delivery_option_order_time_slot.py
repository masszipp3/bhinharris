# Generated by Django 4.2.1 on 2023-06-13 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0011_remove_customer_appartmentname'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_option',
            field=models.CharField(choices=[('now', 'Delivery Now'), ('later', 'Delivery Later')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='time_slot',
            field=models.CharField(blank=True, choices=[('slot1', '10:00 AM - 12:00 PM'), ('slot2', '12:00 PM - 2:00 PM'), ('slot3', '2:00 PM - 4:00 PM'), ('slot4', '4:00 PM - 6:00 PM'), ('slot5', '6:00 PM - 8:00 PM'), ('slot6', '8:00 PM - 10:00 PM'), ('slot7', '10:00 PM - 12:00 AM')], max_length=10, null=True),
        ),
    ]

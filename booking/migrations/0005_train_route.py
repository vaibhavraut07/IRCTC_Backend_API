# Generated by Django 4.2.17 on 2024-12-06 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_remove_seat_is_booked_booking_destination_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='train',
            name='route',
            field=models.JSONField(blank=True, null=True),
        ),
    ]

# Generated by Django 4.2.17 on 2024-12-06 15:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_train_available_seats_alter_train_destination_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seat',
            name='is_booked',
        ),
        migrations.AddField(
            model_name='booking',
            name='destination',
            field=models.CharField(blank=True, default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='booking',
            name='route',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='source',
            field=models.CharField(blank=True, default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='seat',
            name='destination',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='seat',
            name='source',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='seat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.seat'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='train',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.train'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

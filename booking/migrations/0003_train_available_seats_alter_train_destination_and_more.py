# Generated by Django 4.2.17 on 2024-12-06 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_train_seat_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='train',
            name='available_seats',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='train',
            name='destination',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='train',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='train',
            name='source',
            field=models.CharField(max_length=100),
        ),
    ]

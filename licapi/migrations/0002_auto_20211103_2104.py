# Generated by Django 3.2.8 on 2021-11-03 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mac_address',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='user',
            name='platform_architecture',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='platform_release',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='platform_system',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='processor',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='user',
            name='ram',
            field=models.CharField(blank=True, max_length=32),
        ),
    ]

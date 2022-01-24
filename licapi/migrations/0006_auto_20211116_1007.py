# Generated by Django 3.2.8 on 2021-11-16 05:07

import django.contrib.postgres.fields
from django.db import migrations, models
import licapi.models


class Migration(migrations.Migration):

    dependencies = [
        ('licapi', '0005_auto_20211116_0527'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegrambot',
            name='license_code',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, default=licapi.models.get_license_code_default, size=None),
        ),
        migrations.AddField(
            model_name='telegrambot',
            name='listening',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='telegrambot',
            name='tg_chat_id',
            field=models.BigIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='telegrambot',
            name='tg_username',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
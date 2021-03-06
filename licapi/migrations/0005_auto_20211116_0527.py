# Generated by Django 3.2.8 on 2021-11-16 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licapi', '0004_license_obtainedtimes'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramBot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tg_user_id', models.BigIntegerField()),
                ('banned', models.BooleanField(default=False)),
                ('previous_command', models.CharField(default='Empty', max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='tg_bot_enabled',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='tg_bot_errors',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]

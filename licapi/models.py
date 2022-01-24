import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
class License(models.Model):
    license_code = models.CharField(max_length=200)
    obtained = models.BooleanField(default=False)
    obtainedTimes = models.IntegerField(default=0, blank=True)

class User(models.Model):
    computer_name = models.CharField(max_length=200)
    platform_system = models.CharField(max_length=100, blank=True)
    platform_release = models.CharField(max_length=100, blank=True)
    platform_architecture = models.CharField(max_length=100, blank=True)
    mac_address = models.CharField(max_length=50, blank=True)
    processor = models.CharField(max_length=200, blank=True)
    ram = models.CharField(max_length=32, blank=True)
    
    # How many times user have updated his computer specs in DB
    editedTimes = models.IntegerField(default=0, blank=True)
    
    register_date = models.DateTimeField('date registered')
    license_code = models.OneToOneField(
        License,
        on_delete=models.CASCADE,
        primary_key=True
    )
    
    tg_bot_enabled = models.BooleanField(default=False, blank=True)
    tg_bot_errors = models.IntegerField(default=0, blank=True)
    
    def __str__(self):
        return f"User's computer name: {self.computer_name}, \
register date: {self.register_date}."

    @admin.display(
        boolean=True,
        ordering="register_date",
        description="Registered within 1 day?"
    )
    def was_registered_within_one_day(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.register_date <= now
    
def get_license_code_default():
    return list(["/empty/"])
class TelegramBot(models.Model):
    tg_user_id = models.BigIntegerField()
    tg_chat_id = models.BigIntegerField()
    tg_username = models.CharField(max_length=200, blank=True)
    banned = models.BooleanField(default=False)
    listening = models.BooleanField(default=False)
    license_code = ArrayField(models.CharField(max_length=200), blank=True, default=get_license_code_default)
    
    previous_command = models.CharField(max_length=200, default="Empty")
    
    
    
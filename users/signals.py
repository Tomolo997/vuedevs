from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Developer

def saveImage(sender, instance, created, **kwargs):
    print(sender)
    print(instance)
    print(created)
    print("PRE SAVE")


pre_save.connect(saveImage, sender=Developer)
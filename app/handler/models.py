import os

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Application(models.Model):
    '''
    for storing details related to application and it's docker container
    and image
    '''
    name = models.CharField(null=True, blank=True, max_length=255)
    repo = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)
    domain = models.CharField(max_length=255, unique=True)
    location = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.repo} {self.branch}'


@receiver(pre_save, sender=Application)
def tranction_handler(sender, instance, **kwargs):
    name = str(instance.repo).split('/')
    name = name[len(name)-1].replace('.git', '')
    print(name)
    instance.name = name
    instance.location = f'/home/ubuntu/{instance.name}/{instance.branch}/'

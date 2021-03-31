import os
import docker

from django.db import models
from django.contrib.auth import AbstractUser


class UserBase(AbstractUser):
    '''
    Inheritace user base
    '''
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


# class Setting(models.Model):
#     '''
#     for base app settings
#     '''
#     network_name = models.CharField(default='HouseNetwork', max_length=255)
#     is_active = models.BooleanField(default=False)


class Application(models.Model):
    '''
    for storing details related to application and it's docker container and image
    '''
    repo = models.CharField()
    branch = models.CharField()
    name = models.CharField()
    domain = models.CharField()
    location = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.repo} {self.branch}'
    # class Meta:
    #     unique_together = ('repo', 'branch',)


def update_app(app):
    home = '/home/lurayy'
    os.chdir(home)
    if not os.path.exists(f'{home}/{app.repo}/'):
        os.system(f'git clone {app.repo}')
    os.chdir(f'{home}/{app.name}')
    os.system(f'git checkout {app.branch}')
    os.system(f'git pull origin {app.branch}')
    os.system(f'sudo service {app.name}-{app.branch} restart')


def create_app(app):
    home = '/home/lurayy'
    os.chdir(home)
    if not os.path.exists(f'{home}/{app.repo}/'):
        os.system(f'git clone {app.repo}')
    os.chdir(f'{home}/{app.name}')
    os.system(f'git checkout {app.branch}')
    os.system(f'git pull origin {app.branch}')
    create_service()
    create_nginx()

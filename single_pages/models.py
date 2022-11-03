from django.db import models
from django.contrib.auth.models import User
import os



class App(models.Model):
    title = models.CharField(max_length=30) #앱 제목
    description = models.TextField() #앱 소개
    logo_image = models.ImageField(upload_to='duksung/images/%Y/%m/%d/', blank=True)
    update_date = models.DateTimeField(auto_now=True)

    developer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'[{self.pk}] : {self.developer} '

    def get_absolute_url(self):
        return f'/duksung/{self.pk}/'

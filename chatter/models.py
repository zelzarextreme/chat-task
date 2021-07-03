from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

class ChatData(models.Model):
    room_name = models.SlugField(max_length=30,null=True,blank=True)
    user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    chunk_number = models.IntegerField(null=True,blank=True)

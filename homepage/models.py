from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class ProfileUser(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='user/%Y/%m/%d', blank=True)
    first_name = models.CharField(max_length=90, blank=True)
    last_name = models.CharField(max_length=90, blank=True)
    name_organization = models.CharField(max_length=90, blank=True)
    type_service = models.CharField(max_length=50, blank=True)
    price = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=90, blank=True)
    link_to_instagram = models.TextField(blank=True)
    contact_details = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('homepage:people_details',
                       args=[self.id])

    def __str__(self):
        return f'{self.user.username} profile'


class Comment(models.Model):
    profile = models.ForeignKey(ProfileUser,
                                on_delete=models.CASCADE,
                                related_name='comments')
    name = models.CharField(max_length=90)
    email = models.EmailField()
    body = models.TextField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'Comment by {self.name} on {self.profile}'

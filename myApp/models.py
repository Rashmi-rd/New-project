from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, blank=True, on_delete=models.CASCADE, unique=True)
    profile_pic = models.ImageField(null=True, default="Download.png")
    date_of_registeration = models.DateTimeField(auto_now_add=True, null=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

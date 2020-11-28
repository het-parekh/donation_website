from django.db.models.signals import post_save,post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(models.signals.post_delete, sender=Post)
def remove_file_from_azure(sender, instance, using, **kwargs):
    instance.main_img.delete(save=False)
    for i in instance.post_img.all():
        i.images.delete(save=False)

@receiver(models.signals.post_delete, sender=Profile)
def remove_profile_file_from_azure(sender, instance, using, **kwargs):
    instance.image.delete(save=False)
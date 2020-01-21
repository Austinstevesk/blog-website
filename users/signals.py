from django.db.models.signals import post_save, post_delete
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

'''@receiver(post_delete, sender=User)
def on_delete(sender, **kwargs):
    instance = kwargs['instance']
    # user is the name of the field file of the user model
    # replace with name of your file field
    instance.User.delete(save=False)'''

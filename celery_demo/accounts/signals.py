from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from celery_demo.accounts.models import ProfileModel

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ProfileModel.objects.create(account=instance)

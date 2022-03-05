from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model
from coreapi.utils import otp_generator

from otp.models import Otp


# @receiver(post_save, sender=get_user_model())
# def save_otp(sender, instance, created, **kwargs):
#     """
#     This signal generates a unique OTP to save in the 'Otp' model
#     for the instance
#     """
#     if created:
#         obj = Otp.objects.create(otp=otp_generator(), user=instance)
#         return obj
#     return None

from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Profile
from .models import Teacher, Courses
from django.core.exceptions import ObjectDoesNotExist


@receiver(post_save, sender=Profile)
def save_teacher(sender, instance, **kwargs):
    try:
        instance.teacher.save()
    except ObjectDoesNotExist:
        if not instance.is_student:
            Teacher.objects.create(profile=instance)
            instance.teacher.save()

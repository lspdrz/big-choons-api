from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Track(Base):
    class MediaType(models.TextChoices):
        APPLE_MUSIC = 'AM', _('AppleMusic')
        SPOTIFY = 'SP', _('Spotify')
        SOUNDCLOUD = 'SO', _('Soundcloud')
        YOUTUBE = 'YT', _('Youtube')

    title = models.CharField(max_length=200)
    source = models.CharField(max_length=500)
    media_type = models.CharField(
        max_length=2,
        choices=MediaType.choices,
        default=MediaType.YOUTUBE,
    )

    def __str__(self):
        return self.title


class UserTrack(Base):
    user = models.ForeignKey(User, related_name="user",
                             on_delete=models.CASCADE)
    track = models.ForeignKey(
        "Track", related_name="track", on_delete=models.CASCADE)
    notes = models.CharField(max_length=280, null=True)
    likes = models.ManyToManyField(User)


class UserFollowing(Base):
    user = models.ForeignKey(
        User, related_name="following", on_delete=models.CASCADE)
    following_user = models.ForeignKey(
        User, related_name="followers", on_delete=models.CASCADE)

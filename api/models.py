from django.db import models
from django.utils.translation import gettext_lazy as _


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(Base):
    username = models.CharField(max_length=30)
    name = models.CharField(max_length=60)
    email = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.username


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
    user = models.ForeignKey(
        "User", related_name="user", on_delete=models.CASCADE)
    track = models.ForeignKey(
        "Track", related_name="track", on_delete=models.CASCADE)
    notes = models.CharField(max_length=280, null=True)
    likes = models.ManyToManyField(User)


class UserFollowing(Base):
    user_id = models.ForeignKey(
        "User", related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(
        "User", related_name="followers", on_delete=models.CASCADE)

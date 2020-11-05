from django.contrib import admin
from .models import Profile, Track, UserTrack, UserFollowing

# Register your models here.
admin.site.register(Profile)
admin.site.register(Track)
admin.site.register(UserTrack)
admin.site.register(UserFollowing)

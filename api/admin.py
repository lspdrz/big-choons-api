from django.contrib import admin
from .models import User, Track, UserTrack, UserFollowing

# Register your models here.
admin.site.register(User)
admin.site.register(Track)
admin.site.register(UserTrack)
admin.site.register(UserFollowing)

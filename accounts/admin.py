from django.contrib import admin
from .models import TeamsInvite, FriendshipInvite, Friendship, User

# Register your models here.
admin.site.register(TeamsInvite)
admin.site.register(FriendshipInvite)
admin.site.register(Friendship)
admin.site.register(User)
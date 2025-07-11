from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

# ========= Abstract =========
class CreatedAtFieldModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
# ========= Abstract =========

class User(AbstractUser):
    PRIVACY_POLICY_CHOICES = (
        ("Opened", "Opened"),
        ("Friends", "Opened only for friends"),
        ("Private", "Private"),
    )
    pidoras = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to="avatar", null=True, blank=True)
    bio = models.CharField(max_length=1500, null=True, blank=True)
    privacy_policy = models.CharField(max_length=15,
                                      choices=PRIVACY_POLICY_CHOICES, default="Opened",
                                      blank=False, null=False)

class Friendship(models.Model):
    id = models.AutoField(primary_key=True)
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friendship1')
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friendship2')

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f'{self.user1.username} + {self.user2.username} = ❤️'

class FriendshipInvite(CreatedAtFieldModel):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name='send_friend_invite')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='receive_friend_invite')

    def __str__(self):
        return f'{self.sender} дружить хочет с {self.receiver}'

    def accept(self):
        Friendship.objects.create(user1=self.sender, user2=self.receiver)
        Friendship.objects.create(user1=self.receiver, user2=self.sender)
        self.delete()

    def reject(self):
        self.delete()

class TeamsInvite(CreatedAtFieldModel):
    STATUS_CHOICES = (
        ("Accepted", "Принято"),
        ("Rejected", "Отклонено"),
        ("Pending", "На рассмотрении")
    )
    id = models.AutoField(primary_key=True)
    sender = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                  verbose_name="Отправитель", related_name="sent_invites")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 verbose_name="Получатель", related_name="received_invites")
    comment = models.CharField(max_length=360, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Accepted")

    class Meta:
        unique_together = ("sender", "receiver")

    def __str__(self):
        return f"{self.sender} sent invite to {self.receiver}!"


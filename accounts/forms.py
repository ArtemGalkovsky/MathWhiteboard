from django import forms
from .models import TeamsInvite, Friendship
from django.forms import ValidationError

class RoomInviteForm(forms.ModelForm):
    class Meta:
        model = TeamsInvite
        fields = [
            "receiver",
            "comment"
        ]

        widgets = {
            "receiver": forms.ChoiceField(choices=(
                ("Выберите дружбана", Friendship.user1),
            )),
            "comment": forms.Textarea(attrs={"rows": 1, "placeholder": "Комментарий дружбану", "maxlength": 360}),
        }

        labels = {
            "receiver": "Получатель",
            "comment": "Комментарий"
        }

class FriendSearchForm(forms.Form):
    query = forms.CharField(max_length=50, required=True, label="Поиск друга",
                            widget=forms.TextInput(attrs={"placeholder": "Имя друга напиши"}))


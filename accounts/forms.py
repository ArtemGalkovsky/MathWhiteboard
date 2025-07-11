from django import forms
from .models import TeamsInvite, Friendship
from django.forms import ValidationError
from MathWhiteboard.config import ACCOUNTS_REGISTRATION_CODE_LENGTH
from .service.registration_utls import get_registration_code_from_email, get_hash_from_email

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


class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        label="Nickname",
        widget=forms.TextInput(attrs={
            'placeholder': 'Your nickname here :)',
            'max_length': 30,
            'id': 'registration_nickname_input',
            'name': 'username',
            'type': 'text',
        })
    )

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Your email here :)',
            'max_length': 50,
            'id': 'registration_email_input',
            'name': 'email',
            'type': 'email',
        })
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 4:
            raise ValidationError('Nickname too short (min 4 characters)')
        if len(username) > 15:
            raise ValidationError('Nickname too long (max 15 characters)')
        return username


class UserEnterRegistrationCodeForm(forms.Form):
    code = forms.CharField(
        label="Enter code",
        widget=forms.TextInput(attrs={
            "placeholder": "Your code here :)",
            'max_length': ACCOUNTS_REGISTRATION_CODE_LENGTH,
            'id': 'registration_code_input',
        })
    )


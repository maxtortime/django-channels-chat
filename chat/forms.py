from django.contrib.auth.forms import UserCreationForm

from chat.models import ChatUser


class ChatUserCreateForm(UserCreationForm):
    class Meta:
        model = ChatUser
        fields = ['username', 'email', 'password1', 'password2', 'nickname']

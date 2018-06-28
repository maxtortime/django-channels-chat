from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, logout
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic import RedirectView, CreateView
from slugify import slugify

from chat.forms import ChatUserCreateForm
from chat.models import ChatUser
from chat.models import Room


class ChatRoomListView(LoginRequiredMixin, ListView):
    model = Room


class CreateChatRoomView(LoginRequiredMixin, CreateView):
    model = Room
    fields = ('name',)
    success_url = reverse_lazy('rooms')

    def form_valid(self, form):
        rep = super().form_valid(form)
        self.object.slug = slugify(self.object.name,
                                   only_ascii=True) + str(self.object.pk)
        self.object.save()
        return rep


class ChatRoomView(LoginRequiredMixin, DetailView):
    model = Room


class IndexView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


class ChatUserCreate(CreateView):
    model = ChatUser
    form_class = ChatUserCreateForm
    success_url = reverse_lazy('rooms')


class LogoutView(RedirectView):
    pattern_name = 'login'

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super().get_redirect_url(*args, **kwargs)

from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from chat.models import Chatroom, Message
from chat.forms import ChatroomForm, MessageForm

# Create your views here.


class Home(ListView, LoginRequiredMixin):
    """ View for Home page with recent Chatrooms """
    context_object_name = 'chatroom'
    model = Chatroom
    template_name = 'chat/home.html'

    def get_queryset(self):
        # Display 5 most recent chatrooms
        filters = {}
        return Chatroom.objects.order_by('-created').filter(**filters)[:5]

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['recent_chatrooms'] = self.get_queryset()
        return context


class ChatroomList(ListView):
    """ View of available chatrooms """
    context_object_name = 'chatroom'
    template_name = 'chat/chatroom_list.html'

    def get_queryset(self):
        # Order all chatrooms by creation time
        all_chatrooms = Chatroom.objects.order_by('-created')
        return all_chatrooms

    def get_context_data(self, **kwargs):
        context = super(ChatroomList, self).get_context_data(**kwargs)
        context['all_chatrooms'] = self.get_queryset()
        return context

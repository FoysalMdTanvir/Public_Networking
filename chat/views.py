from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.contrib import messages
from chat.models import Chatroom, Message
from chat.forms import ChatroomForm, MessageForm

# Create your views here.


class Home(LoginRequiredMixin, ListView):
    """ View for Chat Home page with recent Chatrooms """
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


class ChatroomList(LoginRequiredMixin, ListView):
    """ View of available chatrooms """
    context_object_name = 'chatroom'
    template_name = 'chat/chatroom_list.html'

    def get_queryset(self):

        all_chatrooms = Chatroom.objects.order_by('-created')
        return all_chatrooms

    def get_context_data(self, **kwargs):
        context = super(ChatroomList, self).get_context_data(**kwargs)
        context['all_chatrooms'] = self.get_queryset()
        return context


class ChatroomCreate(LoginRequiredMixin, CreateView):
    """ View to create a new Chatroom """
    model = Chatroom
    fields = ['name', 'info']

    def form_valid(self, form):
        object = form.save(commit=False)

        object.created_by = self.request.user
        object.save()
        self.success_url = reverse_lazy('chat:chatroom', kwargs={'slug': object.slug})
        return super(ChatroomCreate, self).form_valid(form)


class ChatroomView(LoginRequiredMixin, DetailView):
    """ View of Messages in individual Chatroom """
    model = Chatroom
    context_object_name = 'recent_messages'
    context_object_name = 'chatroom'
    template_name = 'chat/chatroom.html'

    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        rooms = Chatroom.objects.filter(slug=self.kwargs['slug'])
        if rooms.exists():
            return rooms[0]
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(ChatroomView, self).get_context_data(**kwargs)
        context['chatroom'] = self.object
        # 50 most recent Messages in Chatroom
        context['recent_messages'] = Message.objects.filter(chatroom=self.object)[:50]
        return context


class MessageCreate(LoginRequiredMixin, CreateView):
    """ View to create a new Message and send to Chatroom """
    model = Message
    fields = ['text']

    def get_context_data(self, **kwargs):
        context = super(MessageCreate, self).get_context_data(**kwargs)

        context['slug'] = self.kwargs['slug']
        return context

    def form_valid(self, form):

        object = form.save(commit=False)
        object.created_by = self.request.user

        message_chatroom_slug = self.kwargs['slug']
        object.chatroom = Chatroom.objects.get(slug=message_chatroom_slug)

        object.save()
        return super(MessageCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('chat:chatroom', kwargs={'slug': self.kwargs['slug']})


class MessageView(LoginRequiredMixin, DetailView):
    """ View to display a Message """
    model = Message
    context_object_name = 'message'
    template_name = 'chat/message.html'

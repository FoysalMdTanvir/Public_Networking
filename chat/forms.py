from django import forms
from chat.models import Chatroom, Message


class ChatroomForm(forms.ModelForm):
    class Meta:
        model = Chatroom
        fields = ('name', 'info')

    def __init__(self, user, *args, **kwargs):
        super(ChatroomForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        obj = super(ChatroomForm, self).save(*args, **kwargs)
        if self.request:
            obj.user = self.request.user
            obj.save()
        return obj


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('text',)

    def __init__(self, user, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        obj = super(MessageForm, self).save(*args, **kwargs)
        if self.request:
            obj.user = self.request.user
            obj.save()
        return obj

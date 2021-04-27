from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, ListView, DetailView, View, TemplateView, DeleteView
from App_Content.models import Category, Content, Comment, Likes
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from App_Login.models import UserProfile
from django.contrib.auth.models import User
# Create your views here.


class CreateContent(LoginRequiredMixin, CreateView):
    model = Content
    template_name = 'App_Content/create_content.html'
    fields = ('category', 'caption_content', 'image')

    def form_valid(self, form):
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user
        blog_obj.save()
        return HttpResponseRedirect(reverse('index'))


@login_required
def content_list(request):
    if request.method == 'GET':
        search = request.GET.get('search', '')
        result = User.objects.filter(username__icontains=search)
    return render(request, 'App_Content/content_list.html', context={'search': search, 'result': result})

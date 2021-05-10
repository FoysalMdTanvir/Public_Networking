from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, ListView, DetailView, View, TemplateView, DeleteView
from App_Content.models import Category, Content, Comment, Likes
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from App_Login.models import UserProfile, Follow

from App_Content.forms import CommentForm
from App_Login.models import UserProfile
from django.contrib.auth.models import User
# Create your views here.


class CreateContent(LoginRequiredMixin, CreateView):
    model = Content
    template_name = 'App_Content/create_content.html'
    fields = ('category', 'caption_content', 'image')

    def form_valid(self, form):
        content_obj = form.save(commit=False)
        content_obj.author = self.request.user
        content_obj.save()
        return HttpResponseRedirect(reverse('App_Content:my_contents'))


class MyContents(LoginRequiredMixin, TemplateView):
    template_name = 'App_Login/profile.html'


@login_required
def content_list(request):
    following_list = Follow.objects.filter(follower=request.user)
    contents = Content.objects.filter(author__in=following_list.values_list('following'))
    liked_content = Likes.objects.filter(user=request.user)
    liked_content_list = liked_content.values_list('content', flat=True)
    if request.method == 'GET':
        search = request.GET.get('search', '')
        result = User.objects.filter(username__icontains=search)
    return render(request, 'App_Content/content_list.html', context={'search': search, 'result': result, 'contents': contents, 'liked_content_list': liked_content_list})


@login_required
def content_details(request, pk):
    content = Content.objects.get(pk=pk)
    comment_form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.content = content
            comment.save()
            return HttpResponseRedirect(reverse('App_Content:content_details', kwargs={'pk': pk}))
    return render(request, 'App_Content/content_details.html', context={'content': content, 'comment_form': comment_form, })


@login_required
def liked(request, pk):
    content = Content.objects.get(pk=pk)
    already_liked = Likes.objects.filter(content=content, user=request.user)
    if not already_liked:
        liked_content = Likes(content=content, user=request.user)
        liked_content.save()
    return HttpResponseRedirect(reverse('index'))


@login_required
def unliked(request, pk):
    content = Content.objects.get(pk=pk)
    already_liked = Likes.objects.filter(content=content, user=request.user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('index'))


class UpdateContent(LoginRequiredMixin, UpdateView):
    model = Content
    fields = ('category', 'caption_content', 'image')
    template_name = 'App_Content/edit_content.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('App_Content:content_details', kwargs={'pk': self.object.pk})


class DeleteContent(LoginRequiredMixin, DeleteView):
    model = Content
    fields = ('category', 'caption_content', 'image')
    template_name = 'App_Content/delete_content.html'

    def get_success_url(self):
        return reverse_lazy('App_Content:content_list')


@login_required
def CategoryView(request, cats):
    category_contents = Content.objects.filter(category__title__contains=cats)
    return render(request, 'App_Content/categories.html', context={'cats': cats.title(), 'category_contents': category_contents})

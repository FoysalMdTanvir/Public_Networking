from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"


class Content(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    caption_content = models.TextField(verbose_name="What is on your mind?")
    image = models.ImageField(upload_to='content_images', verbose_name="Image")
    publish_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publish_date', ]


class Comment(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='content_comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    comment = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-comment_date',)

    def __str__(self):
        return self.comment


class Likes(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="liked_content")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liker_user")

    def __str__(self):
        return self.user + "likes" + self.content

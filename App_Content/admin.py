from django.contrib import admin
from App_Content.models import Category, Content, Comment, Likes

# Register your models here.

admin.site.register(Category)
admin.site.register(Content)
admin.site.register(Comment)
admin.site.register(Likes)

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('App_Login.urls')),
    path('content/', include('App_Content.urls')),
    path('',  views.Index, name='index'),

]

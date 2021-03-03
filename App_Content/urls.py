from django.urls import path
from App_Content import views

app_name = 'App_Content'

urlpatterns = [
    path('', views.content_list, name='content_list'),
]

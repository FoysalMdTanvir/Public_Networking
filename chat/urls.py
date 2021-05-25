from django.urls import path
from chat import views

app_name = 'chat'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('chatrooms/', views.ChatroomList.as_view(), name='chatrooms'),
    path('create/', views.ChatroomCreate.as_view(), name='chatroom_create_form'),
    path('chatrooms/<slug:slug>', views.ChatroomView.as_view(), name='chatroom'),
    path('chatrooms/<slug:slug>/create', views.MessageCreate.as_view(), name='message_create_form'),
]

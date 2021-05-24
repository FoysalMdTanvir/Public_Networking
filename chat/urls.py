from django.urls import path
from chat import views

app_name = 'chat'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('chatrooms/', views.ChatroomList.as_view(), name='chatrooms')
]

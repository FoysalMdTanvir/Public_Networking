from django.urls import path
from App_Content import views

app_name = 'App_Content'

urlpatterns = [
    path('', views.content_list, name='content_list'),
    path('write/', views.CreateContent.as_view(), name='create_content'),
    path('details/<pk>', views.content_details, name='content_details'),
    path('liked/<pk>/', views.liked, name='liked'),
    path('unliked/<pk>/', views.unliked, name='unliked'),
    path('edit/<pk>/', views.UpdateContent.as_view(), name='edit_content'),
    path('delete/<pk>/', views.DleteContent.as_view(), name='delete_content'),
]

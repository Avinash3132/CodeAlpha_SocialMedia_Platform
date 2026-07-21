from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.feed, name='feed'),
    path('post/create/', views.feed, name='create_post'),
    path('post/<int:post_id>/', views.feed, name='post_detail'),
    path('post/<int:post_id>/like/', views.feed, name='like_post'),
    path('post/<int:post_id>/edit/', views.feed, name='edit_post'),
    path('post/<int:post_id>/delete/', views.feed, name='delete_post'),
]
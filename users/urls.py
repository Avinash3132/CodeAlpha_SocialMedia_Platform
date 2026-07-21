from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_view, name='search'),
    path('suggested/', views.suggested_users, name='suggested'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/follow/', views.follow_toggle, name='follow_toggle'),
    path('profile/<str:username>/followers/', views.followers_list, name='followers'),
    path('profile/<str:username>/following/', views.following_list, name='following'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),
]
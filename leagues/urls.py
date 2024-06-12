from django.urls import path
from . import views

urlpatterns = [
    path('league/<str:pk>/', views.league_profile, name='league'),
    path('league/<str:pk>/edit', views.edit_league, name='edit_league'),
    path('league/register', views.create_league, name='create_league'),
]
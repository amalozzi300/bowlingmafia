from django.urls import path
from . import views

urlpatterns = [
    path('league/register/', views.create_league, name='create_league'),
    path('league/<str:pk>/', views.league_profile, name='league'),
    path('league/<str:pk>/edit/', views.edit_league, name='edit_league'),

    path('league/<str:pk>/invite-admin/', views.invite_admin, name='invite_admin'),

    path('league/<str:pk>/register-sidepot/', views.register_sidepot, name='register_league_sidepot'),
    path('league/<str:league_pk>/edit-sidepot/<str:sidepot_pk>/', views.edit_sidepot, name='edit_league_sidepot'),

    path('league/<str:pk>/create-roster/', views.create_roster, name='create_league_roster'),
]
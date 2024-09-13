from django.urls import path

from bowlingmafia.leagues import views

urlpatterns = [
    path(
        'league/register/',
        views.create_league,
        name='create_league',
    ),
    path(
        'league/<str:league_slug>/edit/',
        views.edit_league,
        name='edit_league',
    ),
]

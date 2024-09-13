from django.urls import path

from bowlingmafia.events import views

urlpatterns = [
    path(
        'event/<str:event_slug>/',
        views.event_homepage,
        name='event_home',
    ),
    path(
        'event/<str:event_slug>/invite-admin/',
        views.invite_admin,
        name='invite_admin',
    ),
    path(
        'event/<str:event_slug>/register-sidepot/',
        views.register_sidepot,
        name='register_sidepot',
    ),
    path(
        'event/<str:event_slug>/edit-sidepot/<str:sidepot_slug>/',
        views.edit_sidepot,
        name='edit_sidepot',
    ),
    path(
        'event/<str:event_slug>/roster/<str:roster_slug>/',
        views.roster_homepage,
        name='roster_home',
    ),
    path(
        'event/<str:event_slug>/roster/<str:roster_slug>/handle_close',
        views.handle_close_registration,
        name='handle_close_registration',
    ),
    path(
        'event/<str:event_slug>/roster/<str:roster_slug>/register/',
        views.create_roster_entry,
        name='register_roster_entry',
    ),
    path(
        'event/<str:event_slug>/roster/<str:roster_slug>/input_scores',
        views.user_game_score_input,
        name='game_input',
    ),
    path(
        'event/<str:event_slug>/roster/<str:roster_slug>/score_verification',
        views.score_verification,
        name='score_verification',
    ),
]

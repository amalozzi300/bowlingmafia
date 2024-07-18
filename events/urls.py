from django.urls import path
from . import views

urlpatterns = [
    path('event/<str:event_slug>/', views.event_homepage, name='event_home'),

    path('event/<str:event_slug>/invite-admin/', views.invite_admin, name='invite_admin'),

    path('event/<str:event_slug>/register-sidepot/', views.register_sidepot, name='register_sidepot'),
    path('event/<str:event_slug>/edit-sidepot/<str:sidepot_slug>/', views.edit_sidepot, name='edit_sidepot'),

    path('event/<str:event_slug>/create-roster/', views.create_roster, name='create_roster'),
    path('event/<str:event_slug>/roster/<str:roster_slug>/', views.roster_homepage, name='roster_home'),
    path('event/<str:event_slug>/roster/<str:roster_slug>/register/', views.create_roster_entry, name='register_roster_entry'),
]
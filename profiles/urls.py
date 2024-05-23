from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

    path('profile/<str:pk>/', views.user_profile, name='user_profile'),
    path('account/', views.user_account, name='account'),
    path('edit-account/', views.edit_account, name='edit_account'),

    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:pk>/', views.view_message, name='message'),
    path('create-message/<str:pk>/', views.create_message, name='create_message'),
]
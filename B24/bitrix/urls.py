from django.urls import path

from . import views

app_name = 'bitrix'

urlpatterns = [
    path('', views.index, name='index'),
    path('auth_redir/', views.auth_redir, name='auth_redir'),
    path('b24_auth/', views.auth_b24, name='auth'),
    path('users/', views.show_users, name='users')
]

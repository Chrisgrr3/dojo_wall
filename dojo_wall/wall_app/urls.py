from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('process_user', views.process_user),
    path('wall', views.success),
    path('login_user', views.login),
    path('logout', views.logout),
    path('post_message', views.post_message),
    path('post_comment', views.post_comment)
]

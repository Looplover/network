
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name="post"),
    path("edit", views.edit, name="edit"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("follow/<int:id>", views.follow, name="follow"),
    path("unfollow/<int:id>", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    path("likes", views.likes, name="likes")
]

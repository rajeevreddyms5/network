
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name="post"),
    path("profile", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("followUnfollow/<str:username>/<str:status>/", views.followUnfollow, name="followUnfollow"),
    
    # API Routes
    path("posts/<int:post_id>", views.posts, name="posts"),
    path("likes/<int:post_id>", views.likes, name="likes"),
]

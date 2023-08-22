from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Posts, UserProfile


def index(request):
    return render(request, "network/index.html", {
        # filter posts by created_at date
        "posts": Posts.objects.order_by("-created_at").all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


# create view function for post
def post(request):
    
    # get post data
    if request.method == 'POST':
        var = request.POST['content']
        if var:
            # save var to database
            user = User.objects.get(id=request.user.id)
            post = Posts()
            post.content = var
            post.author = user
            post.save()     
        
    # redirect to index
    return HttpResponseRedirect(reverse(index))


# create profile view function that renders the profile page
def profile(request):
    # get current user id
    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        return HttpResponseRedirect(reverse("index"))
    
    # get current user
    user = User.objects.get(id=user_id)

    # get all followers to the current user
    followed_by = list(user.followed_by.all())
    
    # get all users current user is following
    following = list(user.following.all())
    
    # get posts of the current user
    posts = list(user.authored_posts.order_by("-created_at").all())
    
    # get all users except current user
    users = User.objects.exclude(id=user_id).exclude(username="rajeev")
    
    # for each user in users check whether they are followed by the current user
    userList = []
    for name in users:
        print(name)
        if len(following) != 0:
            for a in following:
                print(a)
                if str(name) == str(a):
                    userList.append([name, True])
                else:
                    userList.append([name, False])
        else:
            userList.append([name, False])
            
    print(userList)
    
    return render(request, "network/profile.html", {
        "followed_by": len(followed_by),
        "following": len(following),
        "no_posts": len(posts),
        "posts": user.authored_posts.order_by("-created_at").all(),
        "users": userList
    })
        
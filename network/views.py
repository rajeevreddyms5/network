from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json
from django.views.decorators.csrf import csrf_exempt

from .models import User, Posts, UserProfile


def index(request):
    # get all posts by created data in reverse chronological order
    all_posts = Posts.objects.order_by("-created_at").all()
    paginator = Paginator(all_posts, 10) # show 10 posts per page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.user.is_authenticated: 
        return render(request, "network/index.html", {
            "posts": page_obj,
            "current_user": User.objects.get(id=request.user.id),
        })
    else:
        return render(request, "network/index.html", {
            "posts": page_obj,
            "current_user": None,
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


# create view function for post (just like a button function)
@login_required
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
@login_required
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
    templist = []
    if len(following) != 0:
        for name in users:
            for a in following:
                if str(name) == str(a):
                    userList.append([name, True])
                    break
            
            for x in userList:
                templist.append(x[0])
            if name not in templist:
                userList.append([name, False])
    
    if len(following) == 0:
        for name in users:
            userList.append([name, False])

    # Pagination
    all_posts = user.authored_posts.order_by("-created_at").all()
    paginator = Paginator(all_posts, 10) # show 10 posts per page
        
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # render httpresponse with context
    return render(request, "network/profile.html", {
        "followed_by": len(followed_by),
        "following": len(following),
        "no_posts": len(posts),
        "posts": page_obj,
        "users": userList,
        "current_user": User.objects.get(id=request.user.id),
    })


# following view that renders following page with context of users following by the current user
@login_required
def following(request):
    # get current user id
    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        return HttpResponseRedirect(reverse("index"))
    
    # get current user
    user = User.objects.get(id=user_id)
    
    # get all the users that the current user is following
    following = list(user.following.all())

    # create empty list
    following_post_list = []

    # loop through each user in following and append all the posts to the following_post_list
    for name in following:
        temp_user = User.objects.get(username=name)
        for post in temp_user.authored_posts.order_by("-created_at").all():
            following_post_list.append(post)
    
    # Pagination
    all_posts = following_post_list
    paginator = Paginator(all_posts, 10) # show 10 posts per page
        
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/following.html", {
        "posts": page_obj,
        "no_posts": len(following_post_list),
        "current_user": User.objects.get(id=request.user.id),
    })
    

# create follow or unfollow button function
@login_required
def followUnfollow(request, username, status):
    
    # get current userid
    current_user = User.objects.get(id=request.user.id)
    
    # get username id from username
    user = User.objects.get(username=username)
    
    if status == "True":
        userprofile = UserProfile.objects.get(user_name=current_user, follows=user)
        userprofile.delete()
    else:
        userprofile = UserProfile.objects.create(user_name=current_user, follows=user)
        userprofile.save()
    
    return HttpResponseRedirect(reverse("profile"))


# create api view function to fetch post data
def posts(request, post_id):
    
     # Query for requested email
    try:
        post = Posts.objects.get(pk=post_id)
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())
    

    # if the method is PUT then save the post content
    elif request.method == "PUT":
        data = json.loads(request.body)
        post.content = data["content"]
        post.save()
        return HttpResponse(status=204)
    
    # Post must be via GET or PUT
    else:
        return JsonResponse({
           "error": "GET or PUT request required."
        }, status=400)



# create function to put likes on posts
@login_required
def likes(request, post_id):

    # get userid
    current_user = User.objects.get(id=request.user.id)
    print(current_user)

     # Query for requested email
    try:
        post = Posts.objects.get(pk=post_id)
        print(post)
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # get likes
    likes = post.liked.all()
    print(likes)

    # if the method is PUT then save the user liked that post
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("liked") == "false":
            post.liked.add(current_user)
            post.save()
            print(f"successfully added {current_user} from {post}")
            return HttpResponse(status=204)
        else:
            post.liked.remove(current_user)
            post.save()
            print(f"successfully removed {current_user} from {post}")
            return HttpResponse(status=204)
    else:
        return JsonResponse({
           "error": "PUT request required."
        }, status=400)

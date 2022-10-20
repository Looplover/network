import re
import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post, Comment, Follow


def index(request):
    posts = Post.objects.all().order_by('id').reverse()
    p = Paginator(posts, 10)
    p_num = request.GET.get("page")
    page_obj = p.get_page(p_num)
    
    if request.user.is_authenticated:
        user_posts = Post.objects.filter(sender=request.user)
        return render(request, "network/index.html", {
            "page_obj": page_obj,
            "userposts": user_posts
        })
    else:
        return render(request, "network/index.html", {
            "page_obj": page_obj
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
            user = User.objects.create(username=username, email=email, password=password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def post(request):
    if request.method == "POST":
        user = request.user
        subject= request.POST["subject"]
        body = request.POST["body"]
        post = Post.objects.create(sender=user, subject=subject, body=body, likes=0)
        post.save()
    return index(request)

@csrf_exempt
def edit(request):
    if request.method == "POST":
        data = json.loads(request.body)
        key = data.get("num")
        subject = data.get("subject")
        body = data.get("body")
        post = Post.objects.get(pk = key)
        post.subject = subject
        post.body = body
        post.save()

    return HttpResponseRedirect(reverse("index"))

def profile(request, id):
    sender = User.objects.get(pk = id)
    posts = Post.objects.filter(sender = sender).order_by('-timestamp')
    Followers = Follow.objects.filter(following = sender)
    Following = Follow.objects.filter(follower = sender)
    followers = Followers.count()
    following = Following.count()
    follow = False
    for Follower in Followers:
        if Follower.follower == request.user:
            follow = True
    return render(request, "network/profile.html", {
        "sender": sender,
        "posts": posts,
        "follow": follow,
        "followers": followers,
        "following": following
    })

def follow(request, id):
    sender = User.objects.get(pk = id)
    follow = Follow.objects.create(follower=request.user, following=sender)
    follow.save()
    return profile(request, id)

def unfollow(request, id):
    sender = User.objects.get(pk = id)
    follow = Follow.objects.get(follower=request.user, following=sender)
    follow.delete()
    return profile(request, id)

def following(request):
    if request.user.is_authenticated:
        follows = Follow.objects.filter(follower = request.user)
        postss = []
        for follow in follows:
            postss.append(Post.objects.filter(sender = follow.following))

    return render(request, "network/following.html", {
        "postss":postss
    })

@csrf_exempt
def likes(request):
    if request.method == "POST":
        data = json.loads(request.body)
        id = data.get("id")
        post = Post.objects.get(pk = id)
        task = data.get("task")
        if task == "like":
            post.likes += 1
            post.save()
        else:
            if post.likes > 0:
                post.likes -= 1
                post.save()
        
    return index(request)
            


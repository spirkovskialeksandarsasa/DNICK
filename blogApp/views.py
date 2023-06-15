from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from .models import BlogPost, Block, BlogUser
from .forms import PostForm, BlockForm


def posts(request: WSGIRequest):
    user = request.user
    blocked_users = Block.objects.filter(blocker__user=request.user).values_list("blocked__user", flat=True)
    blocked_users = list(blocked_users)  # Convert to list
    visible_posts = BlogPost.objects.exclude(user__user__in=blocked_users).exclude(user__user=user)

    return render(request, "posts.html", {"posts": visible_posts})


def profile(request: WSGIRequest):
    user = BlogUser.objects.get(user=request.user)
    visible_posts = BlogPost.objects.filter(user=user)

    return render(request, "profile.html", {"user": user, "posts": visible_posts})


def add_post(request: WSGIRequest):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = BlogUser.objects.get(user=request.user)
            post.save()
            return redirect("posts")
    else:
        form = PostForm()

    return render(request, "addpost.html", {"form": form})

def blocked(request: WSGIRequest):
    if request.method == "POST":
        form_data = BlockForm(data=request.POST, files=request.FILES)

        if form_data.is_valid():
            block = form_data.save(commit=False)
            block.blocker = BlogUser.objects.get(user=request.user)
            block.save()

            return redirect("blocked")

    blocks = Block.objects.filter(blocker__user=request.user)
    blocked_users = BlogUser.objects.filter(user__in=blocks.values_list("blocked__user", flat=True))

    return render(request, "blockedusers.html", {"form": BlockForm, "users": blocked_users})

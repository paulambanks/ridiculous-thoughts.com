from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.mail import send_mail, BadHeaderError
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from website.models import Post

# Create your views here.


def private_posts_list(request):
    """The page with all blog posts, visible to all"""
    template = 'friends/private_post_list.html'
    post_list = Post.objects.filter(author=request.user, status='Published', privacy='Private').order_by('-created')
    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 6)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, template, {'posts': posts})


def friends_posts_list(request):
    """The page with all blog posts, visible to all"""
    template = 'friends/friends_post_list.html'
    post_list = Post.objects.filter(status='Published', privacy='Friends').order_by('-created')
    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 6)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, template, {'posts': posts})


def individual_friend_post_list(request, user):
    """The page with all blog posts, visible to all"""
    template = 'friends/friends_post_list.html'
    post_list = Post.objects.filter(author=user, status='Published', privacy='Friends').order_by('-created')
    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 6)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, template, {'posts': posts})

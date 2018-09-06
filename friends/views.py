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


@login_required
def private_posts_list(request):
    """The page with all blog posts, visible to all"""
    template = 'friends/private_post_list.html'
    post_list = Post.objects.filter(author=request.user, status='Published',).order_by('-updated')
    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 6)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, template, {'posts': posts})


@login_required
def private_tagged_posts_list(request, tag_id):
    template = 'friends/private_post_list.html'
    """
    The PUBLIC page containing all blog posts with selected tag. Access is granted to both authorised users and visitors.
    """
    # TO DO: Each page consists of 6 posts. Should introduce infinite scrolling? or more posts per page?
    post_list = Post.objects.filter(author=request.user, status='Published', tags=tag_id).order_by('-updated')
    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 6)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts
    }

    return render(request, template, context)


@login_required
def friends_posts_list(request):
    """The page with all blog posts, visible to all"""
    template = 'friends/friends_post_list.html'
    post_list = Post.objects.filter(status='Published', privacy='Friends').order_by('-updated')
    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 6)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, template, {'posts': posts})


@login_required
def friends_tagged_posts_list(request, tag_id):
    template = 'website/post_list.html'
    """
    The PUBLIC page containing all blog posts with selected tag. Access is granted to both authorised users and visitors.
    """
    # TO DO: Each page consists of 6 posts. Should introduce infinite scrolling? or more posts per page?
    post_list = Post.objects.filter(status='Published', privacy='Friends', tags=tag_id).order_by('-updated')
    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 6)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts
    }

    return render(request, template, context)


@login_required
def individual_friend_post_list(request, user):
    """The page with all blog posts, visible to all"""
    template = 'friends/friends_post_list.html'
    post_list = Post.objects.filter(author=user, status='Published', privacy='Friends').order_by('-updated')
    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 6)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, template, {'posts': posts})

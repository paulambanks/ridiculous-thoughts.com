from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.mail import send_mail, BadHeaderError
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from website.models import Post
from accounts.models import UserProfile

# Create your views here.


@login_required
def private_posts_list(request):
    template = 'friends/private_posts_list.html'
    """The page with all blog posts, visible to all"""

    post_list = Post.objects.filter(author=request.user, status='Published',).order_by('-updated')
    profile = UserProfile.objects.get(user=request.user)

    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 6)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
        'profile': profile
    }

    return render(request, template, context)


@login_required
def friends_posts_list(request):
    """The page with all blog posts, visible to all"""
    template = 'friends/friends_posts_list.html'
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



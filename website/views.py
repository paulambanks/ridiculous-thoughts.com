from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post
from .forms import PostForm

# Create your views here.

# posts/views.py


def home(request):
    """The home page introduces user to the blog and allows for registration or login"""
    return render(request, 'home.html')


def posts_list(request):
    template = 'website/post_list.html'
    post_list = Post.objects.filter(status='Published').order_by('-created')
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
def post_draft_list(request):
    template = 'website/post_draft_list.html'
    post_list = Post.objects.filter(status='Draft').order_by('created')
    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 6)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, template, {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'website/post_detail.html', {'post': post})


@login_required
def post_new(request):
    template = 'website/post_edit.html'
    if request.method == "POST":
        form = PostForm(request.POST)

        try:
            if form.is_valid():
                if 'cancel' in request.POST:
                    return HttpResponseRedirect(get_success_url())
                else:
                    post = form.save(commit=False)
                    post.author = request.user
                    post.save()
                    return redirect('website:post_detail', pk=post.pk)

        except Exception as e:
            messages.warning(request, 'Post Failed To Save. Error: {}".format(e)')

    else:
        form = PostForm()
    context = {
        'form': form,
    }

    return render(request, template, context)


def get_success_url():
    return reverse('website:posts_list')


@login_required
def post_edit(request, pk):  # also post update
    template = 'website/post_edit.html'
    post = get_object_or_404(Post, pk=pk)

    # Only author of the post can edit the post
    if request.user == post.author:
        # If this is a POST request then process the Form data
        if request.method == "POST":

            # Create a form instance and populate it with data from the request (binding):
            form = PostForm(request.POST, instance=post)

            try:
                # Check if the form is valid:
                if form.is_valid():
                    post = form.save(commit=False)
                    post.author = request.user
                    post.save()
                    messages.success(request, "Your Post Was Successfully Updated")
                    return redirect('website:post_detail', pk=post.pk)

            except Exception as e:
                messages.warning(request, 'Your Post Was Not Saved Due To An Error: {}.format(e)')

        # If this is a GET (or any other method) create the default form.
        else:
            form = PostForm(instance=post)

        context = {
            'form': form,
            'post': post,
        }

        return render(request, template, context)


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    template = 'website/confirmation_publish.html'

    if request.method == "POST":
        post.publish()
        messages.success(request, "This post has been published.")
        return HttpResponseRedirect(reverse('website:posts_list'))

    if request.user != post.author:
        raise PermissionDenied

    context = {
        "post": post
    }

    return render(request, template, context)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    template = 'website/confirmation_delete.html'

    if request.method == "POST":
        post.delete()
        messages.success(request, "This has been deleted.")
        return HttpResponseRedirect(reverse('website:posts_list'))

    if request.user != post.author:
        raise PermissionDenied

    context = {
        "post": post
    }

    return render(request, template, context)

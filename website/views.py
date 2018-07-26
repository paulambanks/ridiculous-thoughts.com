from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.mail import send_mail, BadHeaderError
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.utils import timezone

from .models import Post, TagPost
from .forms import PostForm, ContactForm, TagPostForm

# Create your views here.

# posts/views.py


def home(request):
    """The home page introduces user to the blog and allows for registration or login"""
    return render(request, 'home.html')


def about(request):
    """The page containing information about the author, including online CV and PDF download link"""
    return render(request, 'website/about.html')


def posts_list(request):
    """The page with all blog posts, visible to all"""
    template = 'website/post_list.html'
    post_list = Post.objects.filter(status='Published', privacy='Public').order_by('-updated')
    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 6)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, template, {'posts': posts})


def individual_public_post_list(request, user):
    """The page with all blog posts, visible to all"""
    template = 'website/post_list.html'
    post_list = Post.objects.filter(author=user, status='Published', privacy='Public').order_by('-updated')
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
    if post.privacy == 'Public':
        return render(request, 'website/post_detail.html', {'post': post})
    elif post.privacy == 'Friends' and request.user.is_authenticated:
        return render(request, 'website/post_detail.html', {'post': post})
    elif post.privacy == 'Private' and request.user == post.author:
        return render(request, 'website/post_detail.html', {'post': post})
    else:
        return PermissionDenied


@login_required
def post_draft_list(request):
    """The page with all unpublished yet drafts. Visible only to the admin/staff"""
    template = 'website/post_draft_list.html'
    post_list = Post.objects.filter(status='Draft', author=request.user).order_by('-created')

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
def post_new(request):
    """Create new post is visible only for the admin and logged users"""
    template = 'website/post_edit.html'

    if request.method == "POST":
        form = PostForm(request.POST)
        tag_form = TagPostForm(request.POST)

        try:
            if all([form.is_valid() and tag_form.is_valid()]):
                if 'cancel' in request.POST:
                    return HttpResponseRedirect(get_success_url())
                else:
                    # Save post data from the form to Post DB
                    post = form.save(commit=False)
                    post.author = request.user
                    post.created = timezone.now
                    post.save()

                    tagpost = tag_form.save(commit=False)
                    tagpost.tagged_post_id = post.id
                    tagpost.save()

                    return redirect('website:post_detail', pk=post.pk,)

        except Exception as e:
            messages.warning(request, 'Post Failed To Save. Error: {}".format(e)')

    else:
        form = PostForm()
        tag_form = TagPostForm()
    context = {
        'form': form,
        'tag_form': tag_form,
    }

    return render(request, template, context)


@login_required
def post_edit(request, pk):  # also post update
    template = 'website/post_edit.html'
    post = get_object_or_404(Post, pk=pk)

    if post.author == request.user:

        if request.method == "POST":
            form = PostForm(request.POST, instance=post)

            try:
                if form.is_valid():
                    if 'cancel' in request.POST:
                        return HttpResponseRedirect(get_success_url())
                    else:
                        post = form.save(commit=False)
                        post.author = request.user
                        post.updated = timezone.now
                        post.save()
                        messages.success(request, "Your Post Was Successfully Updated")
                        return redirect('website:post_detail', pk=post.pk)

            except Exception as e:
                messages.warning(request, 'Your Post Was Not Saved Due To An Error: {}.format(e)')

        else:
            form = PostForm(instance=post)

        context = {
            'form': form,
            'post': post,
        }

        return render(request, template, context)
    else:
        raise PermissionDenied


def get_success_url():
    """Return page if creating/edition of post was canceled"""
    return reverse('website:posts_list')


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    template = 'website/confirmation_publish.html'

    if post.author == request.user:

        if request.method == "POST":
            post.publish()
            messages.success(request, "This post has been published.")
            return HttpResponseRedirect(reverse('website:posts_list'))

        context = {
            "post": post
        }

        return render(request, template, context)
    else:
        raise PermissionDenied


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    template = 'website/confirmation_delete.html'

    if post.author == request.user:

        if request.method == "POST":
            post.delete()
            messages.success(request, "This has been deleted.")
            return HttpResponseRedirect(reverse('website:posts_list'))

        context = {
            "post": post
        }

        return render(request, template, context)
    else:
        raise PermissionDenied


def send_email(request):
    """Sends a message to the admin from the user"""
    template = 'website/email.html'
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            name = form.cleaned_data['name']
            message = form.cleaned_data['message']
            if request.user.is_authenticated:
                from_email = request.user.email

                try:
                    message = "User {} with email {} has sent you a message:\n".format(name, from_email) + message
                    send_mail(subject, message, from_email, ['bankspaula576@gmail.com'])
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')

            else:
                email = form.cleaned_data['email']

                try:
                    message = "User {} with email {} has sent you a message:\n".format(name, email) + message
                    send_mail(subject, message, email, ['bankspaula576@gmail.com'])
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')

            return redirect('website:success')

    return render(request, template, {'form': form})


def email_success(request):
    return render(request, 'website/success.html')


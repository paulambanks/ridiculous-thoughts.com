from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import inlineformset_factory

from django.utils import timezone

from accounts.models import UserProfile

from .models import Post, TaggedPost, SharedPost
from .forms import PostForm, ContactForm, TagPostForm, SharedPostForm


# ----------------- MAIN PUBLIC VIEWS -------------------------- #

def about(request):  # TO DO: Add downloadable CV / link to the static website!
    template = 'website/about.html'
    """
    The ABOUT page contains information about the website ADMIN.
    """
    return render(request, template)


def posts_list(request):
    template = 'website/posts_list.html'
    """
    The MAIN HOME PAGE and a PUBLIC page containing all public blog posts. 
    Access is granted to both authorised users and visitors.
    """
    # TO DO: Sorting? Filtering? Search?
    post_list = Post.objects.filter(status='Published', privacy='Public').order_by('-updated')
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


def send_email(request):  # CONTACT FORM
    template = 'website/contact_me.html'
    """
    Sends a message to the website ADMIN from the user or anonymous visitor. 
    Form requires an extra EMAIL and NAME fields if send from an anonymous visitor.
    """

    if request.method == 'GET':
        form = ContactForm()
        # if request.user.is_authenticated:
        #     form.fields['name'] = request.user
        #     form.fields['email'] = request.user.email

    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            name = form.cleaned_data['name']
            message = form.cleaned_data['message']

            if request.user.is_authenticated:  # if contact form send from the logged user
                from_email = request.user.email
                name = request.user.username

                try:
                    message = "User {} with email {} has sent you a message:\n".format(name, from_email) + message
                    send_mail(subject, message, from_email, ['bankspaula576@gmail.com'])
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')

            else:
                email = form.cleaned_data['email']  # if contact form send from an anonymous visitor

                try:
                    message = "User {} with email {} has sent you a message:\n".format(name, email) + message
                    send_mail(subject, message, email, ['bankspaula576@gmail.com'])
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')

            return redirect('website:success')

    context = {
        'form': form
    }

    return render(request, template, context)


def email_success(request):  # CONTACT FORM
    template = 'website/email_success.html'
    """
    Send a success message to the user that filled correctly and send the contact form.
    """
    return render(request, template)


def tagged_posts_list(request, tag_id):
    template = 'website/posts_list.html'
    """
    The PUBLIC page containing all blog posts with selected tag. Access is granted to both authorised users and visitors.
    """
    # TO DO: Each page consists of 6 posts. Should introduce infinite scrolling? or more posts per page?
    if request.user.is_authenticated:
        others_tagged_post_list = Post.objects.filter(status='Published', tags=tag_id).exclude(privacy='Private').order_by('-updated')
        own_tagged_post_list = Post.objects.filter(author=request.user, status='Published', tags=tag_id).order_by('-updated')
        post_list = others_tagged_post_list | own_tagged_post_list
    else:
        post_list = Post.objects.filter(status='Published', privacy='Public', tags=tag_id).order_by('-updated')

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


def shared_post_list(request):
    template = 'website/shared_post_list.html'
    """
    The PUBLIC page containing all blog posts with selected tag. Access is granted to both authorised users and visitors.
    """
    # TO DO: Each page consists of 6 posts. Should introduce infinite scrolling? or more posts per page?

    post_list = Post.objects.filter(status='Published', sharing=request.user).order_by('-author')

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


def individual_author_posts(request, user):
    template = 'website/individual_author_public_posts.html'
    """
    The PUBLIC page with all public posts of an individual author. 
    Access is granted to both authorised users and visitors.
    """

    post_list = Post.objects.filter(author=user, status='Published', privacy='Public').order_by('-updated')

    profile = UserProfile.objects.get(user=user)

    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 6)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'user': 'user',
        'posts': posts,
        'profile': profile,
    }

    return render(request, template, context)


def post_detail(request, pk):
    template = 'website/post_detail.html'
    """
    Page with post details. Depends on the permission, appropriate access is granted to both authorised users and visitors.
    """
    post = get_object_or_404(Post, pk=pk)

    context = {
        'post': post
    }

    if post.privacy == 'Public':
        return render(request, template, context)
    elif post.privacy == 'Friends' and request.user.is_authenticated:
        return render(request, template, context)
    elif post.privacy == 'Private' and request.user == post.author:
        return render(request, template, context)
    else:
        return PermissionDenied


def shared_post_detail(request, id):
    template = 'website/shared_post_detail.html'
    """
    Page with post details. Depends on the permission, appropriate access is granted to both authorised users and visitors.
    """
    if request.user.is_authenticated:
        shared_post = get_object_or_404(Post, id=id)

        context = {
            'shared_post': shared_post,
        }

        return render(request, template, context)


# ----------------- MAIN AUTHOR VIEWS -------------------------- #
@login_required
def post_draft_list(request):
    template = 'website/post_draft_list.html'
    """
    The page with all unpublished yet DRAFTS filtered by the author. 
    Visible only to the logged author.
    """
    post_list = Post.objects.filter(status='Draft', author=request.user).order_by('-created')
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
def post_form(request, pk=None):
    template = 'website/post_form.html'
    """
    Page that allows to create the new post. It is visible only for the logged AUTHOR.
    Page also allows to tag created post. It uses two forms at once.
    """
    # TO DO: Needs to be modified to accommodate multiple tagging at once
    if pk:
        post = Post.objects.get(pk=pk)
        TagInlineFormset = inlineformset_factory(Post, TaggedPost, fields=('tag',), can_delete=True, max_num=6)
    else:
        post = Post()
        TagInlineFormset = inlineformset_factory(Post, TaggedPost, fields=('tag',), can_delete=False, max_num=6)

    post_form = PostForm(instance=post)
    tag_formset = TagInlineFormset(instance=post)

    if request.method == "POST":
        post_form = PostForm(request.POST)

        if pk:
            post_form = PostForm(request.POST, instance=post)

        tag_formset = TagInlineFormset(request.POST, request.FILES)

        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = request.user
            new_post.updated = timezone.now

            tag_formset = TagInlineFormset(request.POST, request.FILES, instance=new_post)
            if tag_formset.is_valid():
                new_post.save()
                tag_formset.save()
                return redirect('website:post_detail', pk=new_post.pk)

    context = {
        "post_form": post_form,
        "tag_formset": tag_formset
    }

    return render(request, template, context)


def get_success_url():  # CANCELLATION
    template = 'website:posts_list'
    """
    Return to the post list page if creating/edition of post was canceled
    """
    return reverse(template)


@login_required
def post_publish(request, pk):
    template = 'website/confirmation_publish.html'
    """
    Page used to confirm the PUBLISH 
    """
    post = Post.objects.get(pk=pk)

    if post.author == request.user:

        if request.method == "POST":
            post.publish()
            messages.success(request, "This post has been published.")
            return HttpResponseRedirect(reverse('website:posts_list'))

        context = {
            "post": post,
            'ready_to_publish': True,
        }

        return render(request, template, context)
    else:
        raise PermissionDenied


@login_required
def post_share(request, pk):
    template = 'website/post_share.html'
    """
    Page used to share a private post with other users. 
    """
    post = Post.objects.get(pk=pk)

    SharedPostInlineFormset = inlineformset_factory(Post, SharedPost, form=SharedPostForm, fields=('user',), can_delete=True,)

    formset = SharedPostInlineFormset(instance=post)

    for form in formset:
        form.fields['user'].queryset = form.fields['user'].queryset.exclude(pk=request.user.pk)

    if post.privacy == "Private" and post.author == request.user:

        if request.method == "POST":
            formset = SharedPostInlineFormset(request.POST, request.FILES, instance=post)

            if formset.is_valid():
                formset.save()
                messages.success(request, "This post has been shared.")
                return redirect('website:post_detail', pk=post.pk, )

        context = {
            'post': post,
            'formset': formset,
        }

        return render(request, template, context)
    else:
        raise PermissionDenied


def error(request):
    template = 'website/post_share_error.html'
    """
    Return to the post list page if there was an error during post sharing. 
    Specifically, if users tried to shared the post with themselves.
    """
    return render(request, template)


@login_required
def post_remove(request, pk):
    template = 'website/confirmation_delete.html'
    """
    Page used to confirm the DELETION.  
    """
    post = get_object_or_404(Post, pk=pk)

    if post.author == request.user:

        if request.method == "POST":
            post.delete()
            messages.success(request, "This has been deleted.")
            return HttpResponseRedirect(reverse('website:posts_list'))

        context = {
            "post": post,
            'ready_to_remove': True,
        }

        return render(request, template, context)
    else:
        raise PermissionDenied

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

from .models import Post, TaggedPost
from .forms import PostForm, ContactForm, TagPostForm, SharedPostForm


# ----------------- MAIN PUBLIC VIEWS -------------------------- #

def home(request):
    template = 'home.html'
    """
    The MAIN HOME PAGE introduces visitor to the blog. 
    Page allows for USER login, use of the CONTACT FORM for the anonymous visitor and access to the ABOUT ME page.
    """
    return render(request, template)


def send_email(request):  # CONTACT FORM
    template = 'website/contact_me.html'
    """
    Sends a message to the website ADMIN from the user or anonymous visitor. 
    Form requires an extra EMAIL and NAME fields if send from an anonymous visitor.
    """

    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            name = form.cleaned_data['name']
            message = form.cleaned_data['message']

            if request.user.is_authenticated:  # if contact form send from the logged user
                from_email = request.user.email

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


def about(request):  # TO DO: Add downloadable CV / link to the static website!
    template = 'website/about.html'
    """
    The ABOUT page contains information about the website ADMIN.
    """
    return render(request, template)


def posts_list(request):
    template = 'website/post_list.html'
    """
    The PUBLIC page containing all public blog posts. Access is granted to both authorised users and visitors.
    """
    # TO DO: Each page consists of 6 posts. Should introduce infinite scrolling? or more posts per page?
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


def tagged_posts_list(request, tag_id):
    template = 'website/post_list.html'
    """
    The PUBLIC page containing all blog posts with selected tag. Access is granted to both authorised users and visitors.
    """
    # TO DO: Each page consists of 6 posts. Should introduce infinite scrolling? or more posts per page?
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


def individual_author_public_posts(request, user):
    template = 'website/post_list.html'
    """
    The PUBLIC page with all public posts of an individual author. 
    Access is granted to both authorised users and visitors.
    """
    # TO DO: Each page consists of 6 posts. Should introduce infinite scrolling? or more posts per page?
    post_list = Post.objects.filter(author=user, status='Published', privacy='Public').order_by('-updated')
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
def post_new(request):
    template = 'website/post_new.html'
    """
    Page that allows to create the new post. It is visible only for the logged AUTHOR.
    Page also allows to tag created post. It uses two forms at once.
    """
    # TO DO: Needs to be modified to accommodate multiple tagging at once

    TagInlineFormset = inlineformset_factory(Post, TaggedPost, fields=('tag',))

    if request.method == "POST":
        form = PostForm(request.POST)
        formset = TagInlineFormset(request.POST)

        try:
            if all([form.is_valid() and formset.is_valid()]):
                if 'cancel' in request.POST:
                    return HttpResponseRedirect(get_success_url())

                else:
                    post = form.save(commit=False)
                    post.author = request.user
                    post.updated = timezone.now
                    formset = TagInlineFormset(request.POST, instance=post)

                    for form in formset:
                        if form.has_changed():
                            post.save()
                            tag = form.save(commit=False)
                            tag.post_id = post.id
                            tag.save()
                        else:
                            post.save()

                    messages.success(request, "Your Post Was Successfully Updated")
                    return redirect('website:post_detail', pk=post.pk)

        except Exception as e:
            messages.warning(request, 'Post Failed To Save. Error: {}".format(e)')

    else:
        form = PostForm()
        formset = TagInlineFormset()
    context = {
        'form': form,
        'formset': formset,
    }

    return render(request, template, context)


@login_required
def post_edit(request, pk):  # also post update
    template = 'website/post_edit.html'
    """
    Page that allows to edit the post. It is visible only for the logged AUTHOR.
    Page also allows to tag the post. It uses two forms at once.
    """
    # TO DO: Needs to be modified to accommodate multiple tagging at once
    post = get_object_or_404(Post, pk=pk)
    # pre-populate UserProfileForm with retrieved user values.

    TagInlineFormset = inlineformset_factory(Post, TaggedPost, fields=('tag',), can_delete=True)

    if post.author == request.user:

        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            formset = TagInlineFormset(request.POST, instance=post)

            try:
                if all([form.is_valid() and formset.is_valid()]):
                    if 'cancel' in request.POST:
                        return HttpResponseRedirect(get_success_url())
                    else:
                        post = form.save(commit=False)
                        post.author = request.user
                        post.updated = timezone.now
                        formset = TagInlineFormset(request.POST, instance=post)

                        for form in formset:
                            if form.has_changed():
                                post.save()
                                tag = form.save(commit=False)
                                tag.post_id = post.id
                                tag.save()
                            else:
                                post.save()

                        messages.success(request, "Your Post Was Successfully Updated")
                        return redirect('website:post_detail', pk=post.pk)

            except Exception as e:
                messages.warning(request, 'Your Post Was Not Saved Due To An Error: {}.format(e)')

        else:
            form = PostForm(instance=post)
            formset = TagInlineFormset()

        context = {
            'form': form,
            'formset': formset,
            'post': post,
        }

        return render(request, template, context)
    else:
        raise PermissionDenied


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
    post = get_object_or_404(Post, pk=pk)

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
def post_share(request, pk):
    template = 'website/post_share.html'
    """
    Page used to share a private post with other users. 
    """
    post = get_object_or_404(Post, pk=pk)

    if post.privacy == "Private" and post.author == request.user:

        if request.method == "POST":
            form = SharedPostForm(request.POST)

            try:
                if form.is_valid():
                    if 'cancel' in request.POST:
                        return HttpResponseRedirect(get_success_url())
                    else:
                        # Saves only one sharing instance from the form to Post DB; NOT IDEAL!
                        # I need to add un-share the post, as well as allow for
                        # multiple sharing happening at once
                        sharedpost = form.save(commit=False)
                        sharedpost.post_id = post.id
                        if sharedpost.user_id == post.author_id:  # WORKS!
                            return redirect('website:error')  # needs better way to show error
                        # I need to add a proper view for unique_together {user, post} error
                        else:
                            sharedpost.save()
                            messages.success(request, "This post has been shared.")
                            return redirect('website:post_detail', pk=post.pk, )

            except Exception as e:
                messages.warning(request, 'Your Post Was Not Saved Due To An Error: {}.format(e)')

        else:
            form = SharedPostForm(instance=post)

        context = {
            'form': form,
            'post': post,
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
            "post": post
        }

        return render(request, template, context)
    else:
        raise PermissionDenied

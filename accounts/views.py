from django.db import transaction
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm, ProfileForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from .models import Profile


def profile_page(request):
    template = 'website/profile_page.html'
    return render(request, template)


@login_required
def new_profile(request):
    template = 'website/edit_profile.html'

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST)

        try:
            if profile_form.is_valid():
                profile = profile_form.save(commit=False)
                profile.user = request.user
                profile.save()
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('website:profile_page', profile.id)

            else:
                messages.error(request, 'Please correct the error below.')

        except Exception as e:
            messages.warning(request, 'Post Failed To Save. Error: {}".format(e)')

    else:
        profile_form = ProfileForm()

    context = {
        'profile_form': profile_form,
    }

    return render(request, template, context)


@login_required
def update_profile(request):
    template = 'website/edit_profile.html'

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)

        try:
            if profile_form.is_valid():
                profile = profile_form.save(commit=False)
                profile.save()
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('website:profile_page')

            else:
                messages.error(request, 'Please correct the error below.')

        except Exception as e:
            messages.warning(request, 'Post Failed To Save. Error: {}".format(e)')

    else:
        profile_form = ProfileForm(instance=request.user.profile)

    context = {
        'profile_form': profile_form,
    }

    return render(request, template, context)



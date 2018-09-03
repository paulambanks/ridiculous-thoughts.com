from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile, CustomUser
from .forms import UserProfileForm
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied


def profile_page(request):
    template = 'website/profile_page.html'
    """
    The MAIN USER PROFILE PAGE introduces basic user information. 
    """
    return render(request, template)


@login_required()  # only logged in users should access this
def edit_user(request, pk):
    """
    Page to EDIT User Profile information.
    """
    template = 'website/profile_update.html'
    user = CustomUser.objects.get(pk=pk)

    # pre-populate UserProfileForm with retrieved user values.
    user_form = UserProfileForm(instance=user)

    ProfileInlineFormset = inlineformset_factory(CustomUser, UserProfile,
                                                 fields=('bio', 'city', 'country', 'avatar'))

    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated and request.user.id == user.id:
        if request.method == "POST":
            user_form = UserProfileForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect('/accounts/profile_page/')

        return render(request, template, {
            "pk": pk,
            "user_form": user_form,
            "formset": formset,
        })
    else:
        return redirect('accounts:profile_error')  # needs better way to show error


def profile_error(request):
    template = 'website/profile_error.html'
    """
    Return error, if users tried to update a profile of someone else.
    """
    return render(request, template)

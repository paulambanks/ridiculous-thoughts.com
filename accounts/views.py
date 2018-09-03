from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile, CustomUser
from .forms import CustomUserChangeForm
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
    The MAIN USER PROFILE PAGE introduces basic user information.
    """
    template = 'website/profile_update.html'
    # querying the User object with pk from url
    # user = CustomUser.objects.get(pk=pk)
    user = request.user

    # pre-populate UserProfileForm with retrieved user values from above.
    user_form = CustomUserChangeForm(instance=user)

    ProfileInlineFormset = inlineformset_factory(CustomUser, UserProfile,
                                                 fields=('bio', 'city', 'country',))

    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated and request.user.id == user.id:
        if request.method == "POST":
            user_form = CustomUserChangeForm(request.POST, instance=user)
            formset = ProfileInlineFormset(request.POST, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, instance=created_user)

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
        raise PermissionDenied